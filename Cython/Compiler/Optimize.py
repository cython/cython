
import cython
cython.declare(UtilityCode=object, EncodedString=object, BytesLiteral=object,
               Nodes=object, ExprNodes=object, PyrexTypes=object, Builtin=object,
               UtilNodes=object, Naming=object)

import Nodes
import ExprNodes
import PyrexTypes
import Visitor
import Builtin
import UtilNodes
import TypeSlots
import Symtab
import Options
import Naming

from Code import UtilityCode
from StringEncoding import EncodedString, BytesLiteral
from Errors import error
from ParseTreeTransforms import SkipDeclarations

import codecs

try:
    from __builtin__ import reduce
except ImportError:
    from functools import reduce

try:
    from __builtin__ import basestring
except ImportError:
    basestring = str # Python 3

def load_c_utility(name):
    return UtilityCode.load_cached(name, "Optimize.c")

class FakePythonEnv(object):
    "A fake environment for creating type test nodes etc."
    nogil = False

def unwrap_coerced_node(node, coercion_nodes=(ExprNodes.CoerceToPyTypeNode, ExprNodes.CoerceFromPyTypeNode)):
    if isinstance(node, coercion_nodes):
        return node.arg
    return node

def unwrap_node(node):
    while isinstance(node, UtilNodes.ResultRefNode):
        node = node.expression
    return node

def is_common_value(a, b):
    a = unwrap_node(a)
    b = unwrap_node(b)
    if isinstance(a, ExprNodes.NameNode) and isinstance(b, ExprNodes.NameNode):
        return a.name == b.name
    if isinstance(a, ExprNodes.AttributeNode) and isinstance(b, ExprNodes.AttributeNode):
        return not a.is_py_attr and is_common_value(a.obj, b.obj) and a.attribute == b.attribute
    return False

class IterationTransform(Visitor.VisitorTransform):
    """Transform some common for-in loop patterns into efficient C loops:

    - for-in-dict loop becomes a while loop calling PyDict_Next()
    - for-in-enumerate is replaced by an external counter variable
    - for-in-range loop becomes a plain C for loop
    """
    PyDict_Size_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_py_ssize_t_type, [
            PyrexTypes.CFuncTypeArg("dict",  PyrexTypes.py_object_type, None),
            ])

    PyDict_Size_name = EncodedString("PyDict_Size")

    PyDict_Size_entry = Symtab.Entry(
        PyDict_Size_name, PyDict_Size_name, PyDict_Size_func_type)

    visit_Node = Visitor.VisitorTransform.recurse_to_children

    def visit_ModuleNode(self, node):
        self.current_scope = node.scope
        self.module_scope = node.scope
        self.visitchildren(node)
        return node

    def visit_DefNode(self, node):
        oldscope = self.current_scope
        self.current_scope = node.entry.scope
        self.visitchildren(node)
        self.current_scope = oldscope
        return node

    def visit_PrimaryCmpNode(self, node):
        if node.is_ptr_contains():

            # for t in operand2:
            #     if operand1 == t:
            #         res = True
            #         break
            # else:
            #     res = False

            pos = node.pos
            res_handle = UtilNodes.TempHandle(PyrexTypes.c_bint_type)
            res = res_handle.ref(pos)
            result_ref = UtilNodes.ResultRefNode(node)
            if isinstance(node.operand2, ExprNodes.IndexNode):
                base_type = node.operand2.base.type.base_type
            else:
                base_type = node.operand2.type.base_type
            target_handle = UtilNodes.TempHandle(base_type)
            target = target_handle.ref(pos)
            cmp_node = ExprNodes.PrimaryCmpNode(
                pos, operator=u'==', operand1=node.operand1, operand2=target)
            if_body = Nodes.StatListNode(
                pos,
                stats = [Nodes.SingleAssignmentNode(pos, lhs=result_ref, rhs=ExprNodes.BoolNode(pos, value=1)),
                         Nodes.BreakStatNode(pos)])
            if_node = Nodes.IfStatNode(
                pos,
                if_clauses=[Nodes.IfClauseNode(pos, condition=cmp_node, body=if_body)],
                else_clause=None)
            for_loop = UtilNodes.TempsBlockNode(
                pos,
                temps = [target_handle],
                body = Nodes.ForInStatNode(
                    pos,
                    target=target,
                    iterator=ExprNodes.IteratorNode(node.operand2.pos, sequence=node.operand2),
                    body=if_node,
                    else_clause=Nodes.SingleAssignmentNode(pos, lhs=result_ref, rhs=ExprNodes.BoolNode(pos, value=0))))
            for_loop.analyse_expressions(self.current_scope)
            for_loop = self(for_loop)
            new_node = UtilNodes.TempResultFromStatNode(result_ref, for_loop)

            if node.operator == 'not_in':
                new_node = ExprNodes.NotNode(pos, operand=new_node)
            return new_node

        else:
            self.visitchildren(node)
            return node

    def visit_ForInStatNode(self, node):
        self.visitchildren(node)
        return self._optimise_for_loop(node, node.iterator.sequence)

    def _optimise_for_loop(self, node, iterator, reversed=False):
        if iterator.type is Builtin.dict_type:
            # like iterating over dict.keys()
            if reversed:
                # CPython raises an error here: not a sequence
                return node
            return self._transform_dict_iteration(
                node, dict_obj=iterator, method=None, keys=True, values=False)

        # C array (slice) iteration?
        if iterator.type.is_ptr or iterator.type.is_array:
            return self._transform_carray_iteration(node, iterator, reversed=reversed)
        if iterator.type in (Builtin.bytes_type, Builtin.unicode_type):
            return self._transform_string_iteration(node, iterator, reversed=reversed)

        # the rest is based on function calls
        if not isinstance(iterator, ExprNodes.SimpleCallNode):
            return node

        if iterator.args is None:
            arg_count = iterator.arg_tuple and len(iterator.arg_tuple.args) or 0
        else:
            arg_count = len(iterator.args)
            if arg_count and iterator.self is not None:
                arg_count -= 1

        function = iterator.function
        # dict iteration?
        if function.is_attribute and not reversed and not arg_count:
            base_obj = iterator.self or function.obj
            method = function.attribute

            is_py3 = self.module_scope.context.language_level >= 3
            keys = values = False
            if method == 'iterkeys' or (is_py3 and method == 'keys'):
                keys = True
            elif method == 'itervalues' or (is_py3 and method == 'values'):
                values = True
            elif method == 'iteritems' or (is_py3 and method == 'items'):
                keys = values = True

            if keys or values:
                return self._transform_dict_iteration(
                    node, base_obj, method, keys, values)

        # enumerate/reversed ?
        if iterator.self is None and function.is_name and \
               function.entry and function.entry.is_builtin:
            if function.name == 'enumerate':
                if reversed:
                    # CPython raises an error here: not a sequence
                    return node
                return self._transform_enumerate_iteration(node, iterator)
            elif function.name == 'reversed':
                if reversed:
                    # CPython raises an error here: not a sequence
                    return node
                return self._transform_reversed_iteration(node, iterator)

        # range() iteration?
        if Options.convert_range and node.target.type.is_int:
            if iterator.self is None and function.is_name and \
                   function.entry and function.entry.is_builtin and \
                   function.name in ('range', 'xrange'):
                return self._transform_range_iteration(node, iterator, reversed=reversed)

        return node

    def _transform_reversed_iteration(self, node, reversed_function):
        args = reversed_function.arg_tuple.args
        if len(args) == 0:
            error(reversed_function.pos,
                  "reversed() requires an iterable argument")
            return node
        elif len(args) > 1:
            error(reversed_function.pos,
                  "reversed() takes exactly 1 argument")
            return node
        arg = args[0]

        # reversed(list/tuple) ?
        if arg.type in (Builtin.tuple_type, Builtin.list_type):
            node.iterator.sequence = arg.as_none_safe_node("'NoneType' object is not iterable")
            node.iterator.reversed = True
            return node

        return self._optimise_for_loop(node, arg, reversed=True)

    PyUnicode_AS_UNICODE_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_py_unicode_ptr_type, [
            PyrexTypes.CFuncTypeArg("s", Builtin.unicode_type, None)
            ])

    PyUnicode_GET_SIZE_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_py_ssize_t_type, [
            PyrexTypes.CFuncTypeArg("s", Builtin.unicode_type, None)
            ])

    PyBytes_AS_STRING_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_char_ptr_type, [
            PyrexTypes.CFuncTypeArg("s", Builtin.bytes_type, None)
            ])

    PyBytes_GET_SIZE_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_py_ssize_t_type, [
            PyrexTypes.CFuncTypeArg("s", Builtin.bytes_type, None)
            ])

    def _transform_string_iteration(self, node, slice_node, reversed=False):
        if slice_node.type is Builtin.unicode_type:
            unpack_func = "PyUnicode_AS_UNICODE"
            len_func = "PyUnicode_GET_SIZE"
            unpack_func_type = self.PyUnicode_AS_UNICODE_func_type
            len_func_type = self.PyUnicode_GET_SIZE_func_type
        elif slice_node.type is Builtin.bytes_type:
            target_type = node.target.type
            if not target_type.is_int:
                # bytes iteration returns bytes objects in Py2, but
                # integers in Py3
                return node
            unpack_func = "PyBytes_AS_STRING"
            unpack_func_type = self.PyBytes_AS_STRING_func_type
            len_func = "PyBytes_GET_SIZE"
            len_func_type = self.PyBytes_GET_SIZE_func_type
        else:
            return node

        unpack_temp_node = UtilNodes.LetRefNode(
            slice_node.as_none_safe_node("'NoneType' is not iterable"))

        slice_base_node = ExprNodes.PythonCapiCallNode(
            slice_node.pos, unpack_func, unpack_func_type,
            args = [unpack_temp_node],
            is_temp = 0,
            )
        len_node = ExprNodes.PythonCapiCallNode(
            slice_node.pos, len_func, len_func_type,
            args = [unpack_temp_node],
            is_temp = 0,
            )

        return UtilNodes.LetNode(
            unpack_temp_node,
            self._transform_carray_iteration(
                node,
                ExprNodes.SliceIndexNode(
                    slice_node.pos,
                    base = slice_base_node,
                    start = None,
                    step = None,
                    stop = len_node,
                    type = slice_base_node.type,
                    is_temp = 1,
                    ),
                reversed = reversed))

    def _transform_carray_iteration(self, node, slice_node, reversed=False):
        neg_step = False
        if isinstance(slice_node, ExprNodes.SliceIndexNode):
            slice_base = slice_node.base
            start = slice_node.start
            stop = slice_node.stop
            step = None
            if not stop:
                if not slice_base.type.is_pyobject:
                    error(slice_node.pos, "C array iteration requires known end index")
                return node

        elif isinstance(slice_node, ExprNodes.IndexNode):
            assert isinstance(slice_node.index, ExprNodes.SliceNode)
            slice_base = slice_node.base
            index = slice_node.index
            start = index.start
            stop = index.stop
            step = index.step
            if step:
                if step.constant_result is None:
                    step = None
                elif not isinstance(step.constant_result, (int,long)) \
                       or step.constant_result == 0 \
                       or step.constant_result > 0 and not stop \
                       or step.constant_result < 0 and not start:
                    if not slice_base.type.is_pyobject:
                        error(step.pos, "C array iteration requires known step size and end index")
                    return node
                else:
                    # step sign is handled internally by ForFromStatNode
                    step_value = step.constant_result
                    if reversed:
                        step_value = -step_value
                    neg_step = step_value < 0
                    step = ExprNodes.IntNode(step.pos, type=PyrexTypes.c_py_ssize_t_type,
                                             value=str(abs(step_value)),
                                             constant_result=abs(step_value))

        elif slice_node.type.is_array:
            if slice_node.type.size is None:
                error(slice_node.pos, "C array iteration requires known end index")
                return node
            slice_base = slice_node
            start = None
            stop = ExprNodes.IntNode(
                slice_node.pos, value=str(slice_node.type.size),
                type=PyrexTypes.c_py_ssize_t_type, constant_result=slice_node.type.size)
            step = None

        else:
            if not slice_node.type.is_pyobject:
                error(slice_node.pos, "C array iteration requires known end index")
            return node

        if start:
            if start.constant_result is None:
                start = None
            else:
                start = start.coerce_to(PyrexTypes.c_py_ssize_t_type, self.current_scope)
        if stop:
            if stop.constant_result is None:
                stop = None
            else:
                stop = stop.coerce_to(PyrexTypes.c_py_ssize_t_type, self.current_scope)
        if stop is None:
            if neg_step:
                stop = ExprNodes.IntNode(
                    slice_node.pos, value='-1', type=PyrexTypes.c_py_ssize_t_type, constant_result=-1)
            else:
                error(slice_node.pos, "C array iteration requires known step size and end index")
                return node

        if reversed:
            if not start:
                start = ExprNodes.IntNode(slice_node.pos, value="0",  constant_result=0,
                                          type=PyrexTypes.c_py_ssize_t_type)
            # if step was provided, it was already negated above
            start, stop = stop, start

        ptr_type = slice_base.type
        if ptr_type.is_array:
            ptr_type = ptr_type.element_ptr_type()
        carray_ptr = slice_base.coerce_to_simple(self.current_scope)

        if start and start.constant_result != 0:
            start_ptr_node = ExprNodes.AddNode(
                start.pos,
                operand1=carray_ptr,
                operator='+',
                operand2=start,
                type=ptr_type)
        else:
            start_ptr_node = carray_ptr

        if stop and stop.constant_result != 0:
            stop_ptr_node = ExprNodes.AddNode(
                stop.pos,
                operand1=ExprNodes.CloneNode(carray_ptr),
                operator='+',
                operand2=stop,
                type=ptr_type
                ).coerce_to_simple(self.current_scope)
        else:
            stop_ptr_node = ExprNodes.CloneNode(carray_ptr)

        counter = UtilNodes.TempHandle(ptr_type)
        counter_temp = counter.ref(node.target.pos)

        if slice_base.type.is_string and node.target.type.is_pyobject:
            # special case: char* -> bytes
            target_value = ExprNodes.SliceIndexNode(
                node.target.pos,
                start=ExprNodes.IntNode(node.target.pos, value='0',
                                        constant_result=0,
                                        type=PyrexTypes.c_int_type),
                stop=ExprNodes.IntNode(node.target.pos, value='1',
                                       constant_result=1,
                                       type=PyrexTypes.c_int_type),
                base=counter_temp,
                type=Builtin.bytes_type,
                is_temp=1)
        elif node.target.type.is_ptr and not node.target.type.assignable_from(ptr_type.base_type):
            # Allow iteration with pointer target to avoid copy.
            target_value = counter_temp
        else:
            target_value = ExprNodes.IndexNode(
                node.target.pos,
                index=ExprNodes.IntNode(node.target.pos, value='0',
                                        constant_result=0,
                                        type=PyrexTypes.c_int_type),
                base=counter_temp,
                is_buffer_access=False,
                type=ptr_type.base_type)

        if target_value.type != node.target.type:
            target_value = target_value.coerce_to(node.target.type,
                                                  self.current_scope)

        target_assign = Nodes.SingleAssignmentNode(
            pos = node.target.pos,
            lhs = node.target,
            rhs = target_value)

        body = Nodes.StatListNode(
            node.pos,
            stats = [target_assign, node.body])

        relation1, relation2 = self._find_for_from_node_relations(neg_step, reversed)

        for_node = Nodes.ForFromStatNode(
            node.pos,
            bound1=start_ptr_node, relation1=relation1,
            target=counter_temp,
            relation2=relation2, bound2=stop_ptr_node,
            step=step, body=body,
            else_clause=node.else_clause,
            from_range=True)

        return UtilNodes.TempsBlockNode(
            node.pos, temps=[counter],
            body=for_node)

    def _transform_enumerate_iteration(self, node, enumerate_function):
        args = enumerate_function.arg_tuple.args
        if len(args) == 0:
            error(enumerate_function.pos,
                  "enumerate() requires an iterable argument")
            return node
        elif len(args) > 1:
            error(enumerate_function.pos,
                  "enumerate() takes at most 1 argument")
            return node

        if not node.target.is_sequence_constructor:
            # leave this untouched for now
            return node
        targets = node.target.args
        if len(targets) != 2:
            # leave this untouched for now
            return node
        if not isinstance(targets[0], ExprNodes.NameNode):
            # leave this untouched for now
            return node

        enumerate_target, iterable_target = targets
        counter_type = enumerate_target.type

        if not counter_type.is_pyobject and not counter_type.is_int:
            # nothing we can do here, I guess
            return node

        temp = UtilNodes.LetRefNode(ExprNodes.IntNode(enumerate_function.pos,
                                                      value='0',
                                                      type=counter_type,
                                                      constant_result=0))
        inc_expression = ExprNodes.AddNode(
            enumerate_function.pos,
            operand1 = temp,
            operand2 = ExprNodes.IntNode(node.pos, value='1',
                                         type=counter_type,
                                         constant_result=1),
            operator = '+',
            type = counter_type,
            is_temp = counter_type.is_pyobject
            )

        loop_body = [
            Nodes.SingleAssignmentNode(
                pos = enumerate_target.pos,
                lhs = enumerate_target,
                rhs = temp),
            Nodes.SingleAssignmentNode(
                pos = enumerate_target.pos,
                lhs = temp,
                rhs = inc_expression)
            ]

        if isinstance(node.body, Nodes.StatListNode):
            node.body.stats = loop_body + node.body.stats
        else:
            loop_body.append(node.body)
            node.body = Nodes.StatListNode(
                node.body.pos,
                stats = loop_body)

        node.target = iterable_target
        node.item = node.item.coerce_to(iterable_target.type, self.current_scope)
        node.iterator.sequence = enumerate_function.arg_tuple.args[0]

        # recurse into loop to check for further optimisations
        return UtilNodes.LetNode(temp, self._optimise_for_loop(node, node.iterator.sequence))

    def _find_for_from_node_relations(self, neg_step_value, reversed):
        if reversed:
            if neg_step_value:
                return '<', '<='
            else:
                return '>', '>='
        else:
            if neg_step_value:
                return '>=', '>'
            else:
                return '<=', '<'

    def _transform_range_iteration(self, node, range_function, reversed=False):
        args = range_function.arg_tuple.args
        if len(args) < 3:
            step_pos = range_function.pos
            step_value = 1
            step = ExprNodes.IntNode(step_pos, value='1',
                                     constant_result=1)
        else:
            step = args[2]
            step_pos = step.pos
            if not isinstance(step.constant_result, (int, long)):
                # cannot determine step direction
                return node
            step_value = step.constant_result
            if step_value == 0:
                # will lead to an error elsewhere
                return node
            if reversed and step_value not in (1, -1):
                # FIXME: currently broken - requires calculation of the correct bounds
                return node
            if not isinstance(step, ExprNodes.IntNode):
                step = ExprNodes.IntNode(step_pos, value=str(step_value),
                                         constant_result=step_value)

        if len(args) == 1:
            bound1 = ExprNodes.IntNode(range_function.pos, value='0',
                                       constant_result=0)
            bound2 = args[0].coerce_to_integer(self.current_scope)
        else:
            bound1 = args[0].coerce_to_integer(self.current_scope)
            bound2 = args[1].coerce_to_integer(self.current_scope)

        relation1, relation2 = self._find_for_from_node_relations(step_value < 0, reversed)

        if reversed:
            bound1, bound2 = bound2, bound1
            if step_value < 0:
                step_value = -step_value
        else:
            if step_value < 0:
                step_value = -step_value

        step.value = str(step_value)
        step.constant_result = step_value
        step = step.coerce_to_integer(self.current_scope)

        if not bound2.is_literal:
            # stop bound must be immutable => keep it in a temp var
            bound2_is_temp = True
            bound2 = UtilNodes.LetRefNode(bound2)
        else:
            bound2_is_temp = False

        for_node = Nodes.ForFromStatNode(
            node.pos,
            target=node.target,
            bound1=bound1, relation1=relation1,
            relation2=relation2, bound2=bound2,
            step=step, body=node.body,
            else_clause=node.else_clause,
            from_range=True)

        if bound2_is_temp:
            for_node = UtilNodes.LetNode(bound2, for_node)

        return for_node

    def _transform_dict_iteration(self, node, dict_obj, method, keys, values):
        temps = []
        temp = UtilNodes.TempHandle(PyrexTypes.py_object_type)
        temps.append(temp)
        dict_temp = temp.ref(dict_obj.pos)
        temp = UtilNodes.TempHandle(PyrexTypes.c_py_ssize_t_type)
        temps.append(temp)
        pos_temp = temp.ref(node.pos)

        key_target = value_target = tuple_target = None
        if keys and values:
            if node.target.is_sequence_constructor:
                if len(node.target.args) == 2:
                    key_target, value_target = node.target.args
                else:
                    # unusual case that may or may not lead to an error
                    return node
            else:
                tuple_target = node.target
        elif keys:
            key_target = node.target
        else:
            value_target = node.target

        if isinstance(node.body, Nodes.StatListNode):
            body = node.body
        else:
            body = Nodes.StatListNode(pos = node.body.pos,
                                      stats = [node.body])

        # keep original length to guard against dict modification
        dict_len_temp = UtilNodes.TempHandle(PyrexTypes.c_py_ssize_t_type)
        temps.append(dict_len_temp)
        dict_len_temp_addr = ExprNodes.AmpersandNode(
            node.pos, operand=dict_len_temp.ref(dict_obj.pos),
            type=PyrexTypes.c_ptr_type(dict_len_temp.type))
        temp = UtilNodes.TempHandle(PyrexTypes.c_int_type)
        temps.append(temp)
        is_dict_temp = temp.ref(node.pos)
        is_dict_temp_addr = ExprNodes.AmpersandNode(
            node.pos, operand=is_dict_temp,
            type=PyrexTypes.c_ptr_type(temp.type))

        iter_next_node = Nodes.DictIterationNextNode(
            dict_temp, dict_len_temp.ref(dict_obj.pos), pos_temp,
            key_target, value_target, tuple_target,
            is_dict_temp)
        iter_next_node.analyse_expressions(self.current_scope)
        body.stats[0:0] = [iter_next_node]

        if method:
            method_node = ExprNodes.StringNode(
                dict_obj.pos, is_identifier=True, value=method)
            dict_obj = dict_obj.as_none_safe_node(
                "'NoneType' object has no attribute '%s'",
                error = "PyExc_AttributeError",
                format_args = [method])
        else:
            method_node = ExprNodes.NullNode(dict_obj.pos)
            dict_obj = dict_obj.as_none_safe_node("'NoneType' object is not iterable")

        def flag_node(value):
            value = value and 1 or 0
            return ExprNodes.IntNode(node.pos, value=str(value), constant_result=value)

        result_code = [
            Nodes.SingleAssignmentNode(
                pos = node.pos,
                lhs = pos_temp,
                rhs = ExprNodes.IntNode(node.pos, value='0',
                                        constant_result=0)),
            Nodes.SingleAssignmentNode(
                pos = dict_obj.pos,
                lhs = dict_temp,
                rhs = ExprNodes.PythonCapiCallNode(
                    dict_obj.pos,
                    "__Pyx_dict_iterator",
                    self.PyDict_Iterator_func_type,
                    utility_code = UtilityCode.load_cached("dict_iter", "Optimize.c"),
                    args = [dict_obj, flag_node(dict_obj.type is Builtin.dict_type),
                            method_node, dict_len_temp_addr, is_dict_temp_addr,
                            ],
                    is_temp=True,
                )),
            Nodes.WhileStatNode(
                pos = node.pos,
                condition = None,
                body = body,
                else_clause = node.else_clause
                )
            ]

        return UtilNodes.TempsBlockNode(
            node.pos, temps=temps,
            body=Nodes.StatListNode(
                node.pos,
                stats = result_code
                ))

    PyDict_Iterator_func_type = PyrexTypes.CFuncType(
        PyrexTypes.py_object_type, [
            PyrexTypes.CFuncTypeArg("dict",  PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("is_dict",  PyrexTypes.c_int_type, None),
            PyrexTypes.CFuncTypeArg("method_name",  PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("p_orig_length",  PyrexTypes.c_py_ssize_t_ptr_type, None),
            PyrexTypes.CFuncTypeArg("p_is_dict",  PyrexTypes.c_int_ptr_type, None),
            ])


class SwitchTransform(Visitor.VisitorTransform):
    """
    This transformation tries to turn long if statements into C switch statements.
    The requirement is that every clause be an (or of) var == value, where the var
    is common among all clauses and both var and value are ints.
    """
    NO_MATCH = (None, None, None)

    def extract_conditions(self, cond, allow_not_in):
        while True:
            if isinstance(cond, ExprNodes.CoerceToTempNode):
                cond = cond.arg
            elif isinstance(cond, UtilNodes.EvalWithTempExprNode):
                # this is what we get from the FlattenInListTransform
                cond = cond.subexpression
            elif isinstance(cond, ExprNodes.TypecastNode):
                cond = cond.operand
            else:
                break

        if isinstance(cond, ExprNodes.PrimaryCmpNode):
            if cond.cascade is not None:
                return self.NO_MATCH
            elif cond.is_c_string_contains() and \
                   isinstance(cond.operand2, (ExprNodes.UnicodeNode, ExprNodes.BytesNode)):
                not_in = cond.operator == 'not_in'
                if not_in and not allow_not_in:
                    return self.NO_MATCH
                if isinstance(cond.operand2, ExprNodes.UnicodeNode) and \
                       cond.operand2.contains_surrogates():
                    # dealing with surrogates leads to different
                    # behaviour on wide and narrow Unicode
                    # platforms => refuse to optimise this case
                    return self.NO_MATCH
                return not_in, cond.operand1, self.extract_in_string_conditions(cond.operand2)
            elif not cond.is_python_comparison():
                if cond.operator == '==':
                    not_in = False
                elif allow_not_in and cond.operator == '!=':
                    not_in = True
                else:
                    return self.NO_MATCH
                # this looks somewhat silly, but it does the right
                # checks for NameNode and AttributeNode
                if is_common_value(cond.operand1, cond.operand1):
                    if cond.operand2.is_literal:
                        return not_in, cond.operand1, [cond.operand2]
                    elif getattr(cond.operand2, 'entry', None) \
                             and cond.operand2.entry.is_const:
                        return not_in, cond.operand1, [cond.operand2]
                if is_common_value(cond.operand2, cond.operand2):
                    if cond.operand1.is_literal:
                        return not_in, cond.operand2, [cond.operand1]
                    elif getattr(cond.operand1, 'entry', None) \
                             and cond.operand1.entry.is_const:
                        return not_in, cond.operand2, [cond.operand1]
        elif isinstance(cond, ExprNodes.BoolBinopNode):
            if cond.operator == 'or' or (allow_not_in and cond.operator == 'and'):
                allow_not_in = (cond.operator == 'and')
                not_in_1, t1, c1 = self.extract_conditions(cond.operand1, allow_not_in)
                not_in_2, t2, c2 = self.extract_conditions(cond.operand2, allow_not_in)
                if t1 is not None and not_in_1 == not_in_2 and is_common_value(t1, t2):
                    if (not not_in_1) or allow_not_in:
                        return not_in_1, t1, c1+c2
        return self.NO_MATCH

    def extract_in_string_conditions(self, string_literal):
        if isinstance(string_literal, ExprNodes.UnicodeNode):
            charvals = list(map(ord, set(string_literal.value)))
            charvals.sort()
            return [ ExprNodes.IntNode(string_literal.pos, value=str(charval),
                                       constant_result=charval)
                     for charval in charvals ]
        else:
            # this is a bit tricky as Py3's bytes type returns
            # integers on iteration, whereas Py2 returns 1-char byte
            # strings
            characters = string_literal.value
            characters = list(set([ characters[i:i+1] for i in range(len(characters)) ]))
            characters.sort()
            return [ ExprNodes.CharNode(string_literal.pos, value=charval,
                                        constant_result=charval)
                     for charval in characters ]

    def extract_common_conditions(self, common_var, condition, allow_not_in):
        not_in, var, conditions = self.extract_conditions(condition, allow_not_in)
        if var is None:
            return self.NO_MATCH
        elif common_var is not None and not is_common_value(var, common_var):
            return self.NO_MATCH
        elif not var.type.is_int or sum([not cond.type.is_int for cond in conditions]):
            return self.NO_MATCH
        return not_in, var, conditions

    def has_duplicate_values(self, condition_values):
        # duplicated values don't work in a switch statement
        seen = set()
        for value in condition_values:
            if value.constant_result is not ExprNodes.not_a_constant:
                if value.constant_result in seen:
                    return True
                seen.add(value.constant_result)
            else:
                # this isn't completely safe as we don't know the
                # final C value, but this is about the best we can do
                seen.add(getattr(getattr(value, 'entry', None), 'cname'))
        return False

    def visit_IfStatNode(self, node):
        common_var = None
        cases = []
        for if_clause in node.if_clauses:
            _, common_var, conditions = self.extract_common_conditions(
                common_var, if_clause.condition, False)
            if common_var is None:
                self.visitchildren(node)
                return node
            cases.append(Nodes.SwitchCaseNode(pos = if_clause.pos,
                                              conditions = conditions,
                                              body = if_clause.body))

        if sum([ len(case.conditions) for case in cases ]) < 2:
            self.visitchildren(node)
            return node
        if self.has_duplicate_values(sum([case.conditions for case in cases], [])):
            self.visitchildren(node)
            return node

        common_var = unwrap_node(common_var)
        switch_node = Nodes.SwitchStatNode(pos = node.pos,
                                           test = common_var,
                                           cases = cases,
                                           else_clause = node.else_clause)
        return switch_node

    def visit_CondExprNode(self, node):
        not_in, common_var, conditions = self.extract_common_conditions(
            None, node.test, True)
        if common_var is None \
               or len(conditions) < 2 \
               or self.has_duplicate_values(conditions):
            self.visitchildren(node)
            return node
        return self.build_simple_switch_statement(
            node, common_var, conditions, not_in,
            node.true_val, node.false_val)

    def visit_BoolBinopNode(self, node):
        not_in, common_var, conditions = self.extract_common_conditions(
            None, node, True)
        if common_var is None \
               or len(conditions) < 2 \
               or self.has_duplicate_values(conditions):
            self.visitchildren(node)
            return node

        return self.build_simple_switch_statement(
            node, common_var, conditions, not_in,
            ExprNodes.BoolNode(node.pos, value=True, constant_result=True),
            ExprNodes.BoolNode(node.pos, value=False, constant_result=False))

    def visit_PrimaryCmpNode(self, node):
        not_in, common_var, conditions = self.extract_common_conditions(
            None, node, True)
        if common_var is None \
               or len(conditions) < 2 \
               or self.has_duplicate_values(conditions):
            self.visitchildren(node)
            return node

        return self.build_simple_switch_statement(
            node, common_var, conditions, not_in,
            ExprNodes.BoolNode(node.pos, value=True, constant_result=True),
            ExprNodes.BoolNode(node.pos, value=False, constant_result=False))

    def build_simple_switch_statement(self, node, common_var, conditions,
                                      not_in, true_val, false_val):
        result_ref = UtilNodes.ResultRefNode(node)
        true_body = Nodes.SingleAssignmentNode(
            node.pos,
            lhs = result_ref,
            rhs = true_val,
            first = True)
        false_body = Nodes.SingleAssignmentNode(
            node.pos,
            lhs = result_ref,
            rhs = false_val,
            first = True)

        if not_in:
            true_body, false_body = false_body, true_body

        cases = [Nodes.SwitchCaseNode(pos = node.pos,
                                      conditions = conditions,
                                      body = true_body)]

        common_var = unwrap_node(common_var)
        switch_node = Nodes.SwitchStatNode(pos = node.pos,
                                           test = common_var,
                                           cases = cases,
                                           else_clause = false_body)
        return UtilNodes.TempResultFromStatNode(result_ref, switch_node)

    visit_Node = Visitor.VisitorTransform.recurse_to_children


class FlattenInListTransform(Visitor.VisitorTransform, SkipDeclarations):
    """
    This transformation flattens "x in [val1, ..., valn]" into a sequential list
    of comparisons.
    """

    def visit_PrimaryCmpNode(self, node):
        self.visitchildren(node)
        if node.cascade is not None:
            return node
        elif node.operator == 'in':
            conjunction = 'or'
            eq_or_neq = '=='
        elif node.operator == 'not_in':
            conjunction = 'and'
            eq_or_neq = '!='
        else:
            return node

        if not isinstance(node.operand2, (ExprNodes.TupleNode,
                                          ExprNodes.ListNode,
                                          ExprNodes.SetNode)):
            return node

        args = node.operand2.args
        if len(args) == 0:
            return ExprNodes.BoolNode(pos = node.pos, value = node.operator == 'not_in')

        lhs = UtilNodes.ResultRefNode(node.operand1)

        conds = []
        temps = []
        for arg in args:
            try:
                # Trial optimisation to avoid redundant temp
                # assignments.  However, since is_simple() is meant to
                # be called after type analysis, we ignore any errors
                # and just play safe in that case.
                is_simple_arg = arg.is_simple()
            except Exception:
                is_simple_arg = False
            if not is_simple_arg:
                # must evaluate all non-simple RHS before doing the comparisons
                arg = UtilNodes.LetRefNode(arg)
                temps.append(arg)
            cond = ExprNodes.PrimaryCmpNode(
                                pos = node.pos,
                                operand1 = lhs,
                                operator = eq_or_neq,
                                operand2 = arg,
                                cascade = None)
            conds.append(ExprNodes.TypecastNode(
                                pos = node.pos,
                                operand = cond,
                                type = PyrexTypes.c_bint_type))
        def concat(left, right):
            return ExprNodes.BoolBinopNode(
                                pos = node.pos,
                                operator = conjunction,
                                operand1 = left,
                                operand2 = right)

        condition = reduce(concat, conds)
        new_node = UtilNodes.EvalWithTempExprNode(lhs, condition)
        for temp in temps[::-1]:
            new_node = UtilNodes.EvalWithTempExprNode(temp, new_node)
        return new_node

    visit_Node = Visitor.VisitorTransform.recurse_to_children


class DropRefcountingTransform(Visitor.VisitorTransform):
    """Drop ref-counting in safe places.
    """
    visit_Node = Visitor.VisitorTransform.recurse_to_children

    def visit_ParallelAssignmentNode(self, node):
        """
        Parallel swap assignments like 'a,b = b,a' are safe.
        """
        left_names, right_names = [], []
        left_indices, right_indices = [], []
        temps = []

        for stat in node.stats:
            if isinstance(stat, Nodes.SingleAssignmentNode):
                if not self._extract_operand(stat.lhs, left_names,
                                             left_indices, temps):
                    return node
                if not self._extract_operand(stat.rhs, right_names,
                                             right_indices, temps):
                    return node
            elif isinstance(stat, Nodes.CascadedAssignmentNode):
                # FIXME
                return node
            else:
                return node

        if left_names or right_names:
            # lhs/rhs names must be a non-redundant permutation
            lnames = [ path for path, n in left_names ]
            rnames = [ path for path, n in right_names ]
            if set(lnames) != set(rnames):
                return node
            if len(set(lnames)) != len(right_names):
                return node

        if left_indices or right_indices:
            # base name and index of index nodes must be a
            # non-redundant permutation
            lindices = []
            for lhs_node in left_indices:
                index_id = self._extract_index_id(lhs_node)
                if not index_id:
                    return node
                lindices.append(index_id)
            rindices = []
            for rhs_node in right_indices:
                index_id = self._extract_index_id(rhs_node)
                if not index_id:
                    return node
                rindices.append(index_id)

            if set(lindices) != set(rindices):
                return node
            if len(set(lindices)) != len(right_indices):
                return node

            # really supporting IndexNode requires support in
            # __Pyx_GetItemInt(), so let's stop short for now
            return node

        temp_args = [t.arg for t in temps]
        for temp in temps:
            temp.use_managed_ref = False

        for _, name_node in left_names + right_names:
            if name_node not in temp_args:
                name_node.use_managed_ref = False

        for index_node in left_indices + right_indices:
            index_node.use_managed_ref = False

        return node

    def _extract_operand(self, node, names, indices, temps):
        node = unwrap_node(node)
        if not node.type.is_pyobject:
            return False
        if isinstance(node, ExprNodes.CoerceToTempNode):
            temps.append(node)
            node = node.arg
        name_path = []
        obj_node = node
        while isinstance(obj_node, ExprNodes.AttributeNode):
            if obj_node.is_py_attr:
                return False
            name_path.append(obj_node.member)
            obj_node = obj_node.obj
        if isinstance(obj_node, ExprNodes.NameNode):
            name_path.append(obj_node.name)
            names.append( ('.'.join(name_path[::-1]), node) )
        elif isinstance(node, ExprNodes.IndexNode):
            if node.base.type != Builtin.list_type:
                return False
            if not node.index.type.is_int:
                return False
            if not isinstance(node.base, ExprNodes.NameNode):
                return False
            indices.append(node)
        else:
            return False
        return True

    def _extract_index_id(self, index_node):
        base = index_node.base
        index = index_node.index
        if isinstance(index, ExprNodes.NameNode):
            index_val = index.name
        elif isinstance(index, ExprNodes.ConstNode):
            # FIXME:
            return None
        else:
            return None
        return (base.name, index_val)


class EarlyReplaceBuiltinCalls(Visitor.EnvTransform):
    """Optimize some common calls to builtin types *before* the type
    analysis phase and *after* the declarations analysis phase.

    This transform cannot make use of any argument types, but it can
    restructure the tree in a way that the type analysis phase can
    respond to.

    Introducing C function calls here may not be a good idea.  Move
    them to the OptimizeBuiltinCalls transform instead, which runs
    after type analyis.
    """
    # only intercept on call nodes
    visit_Node = Visitor.VisitorTransform.recurse_to_children

    def visit_SimpleCallNode(self, node):
        self.visitchildren(node)
        function = node.function
        if not self._function_is_builtin_name(function):
            return node
        return self._dispatch_to_handler(node, function, node.args)

    def visit_GeneralCallNode(self, node):
        self.visitchildren(node)
        function = node.function
        if not self._function_is_builtin_name(function):
            return node
        arg_tuple = node.positional_args
        if not isinstance(arg_tuple, ExprNodes.TupleNode):
            return node
        args = arg_tuple.args
        return self._dispatch_to_handler(
            node, function, args, node.keyword_args)

    def _function_is_builtin_name(self, function):
        if not function.is_name:
            return False
        env = self.current_env()
        entry = env.lookup(function.name)
        if entry is not env.builtin_scope().lookup_here(function.name):
            return False
        # if entry is None, it's at least an undeclared name, so likely builtin
        return True

    def _dispatch_to_handler(self, node, function, args, kwargs=None):
        if kwargs is None:
            handler_name = '_handle_simple_function_%s' % function.name
        else:
            handler_name = '_handle_general_function_%s' % function.name
        handle_call = getattr(self, handler_name, None)
        if handle_call is not None:
            if kwargs is None:
                return handle_call(node, args)
            else:
                return handle_call(node, args, kwargs)
        return node

    def _inject_capi_function(self, node, cname, func_type, utility_code=None):
        node.function = ExprNodes.PythonCapiFunctionNode(
            node.function.pos, node.function.name, cname, func_type,
            utility_code = utility_code)

    def _error_wrong_arg_count(self, function_name, node, args, expected=None):
        if not expected: # None or 0
            arg_str = ''
        elif isinstance(expected, basestring) or expected > 1:
            arg_str = '...'
        elif expected == 1:
            arg_str = 'x'
        else:
            arg_str = ''
        if expected is not None:
            expected_str = 'expected %s, ' % expected
        else:
            expected_str = ''
        error(node.pos, "%s(%s) called with wrong number of args, %sfound %d" % (
            function_name, arg_str, expected_str, len(args)))

    # specific handlers for simple call nodes

    def _handle_simple_function_float(self, node, pos_args):
        if len(pos_args) == 0:
            return ExprNodes.FloatNode(node.pos, value='0.0')
        if len(pos_args) > 1:
            self._error_wrong_arg_count('float', node, pos_args, 1)
        return node

    class YieldNodeCollector(Visitor.TreeVisitor):
        def __init__(self):
            Visitor.TreeVisitor.__init__(self)
            self.yield_stat_nodes = {}
            self.yield_nodes = []

        visit_Node = Visitor.TreeVisitor.visitchildren
        # XXX: disable inlining while it's not back supported
        def __visit_YieldExprNode(self, node):
            self.yield_nodes.append(node)
            self.visitchildren(node)

        def __visit_ExprStatNode(self, node):
            self.visitchildren(node)
            if node.expr in self.yield_nodes:
                self.yield_stat_nodes[node.expr] = node

        def __visit_GeneratorExpressionNode(self, node):
            # enable when we support generic generator expressions
            #
            # everything below this node is out of scope
            pass

    def _find_single_yield_expression(self, node):
        collector = self.YieldNodeCollector()
        collector.visitchildren(node)
        if len(collector.yield_nodes) != 1:
            return None, None
        yield_node = collector.yield_nodes[0]
        try:
            return (yield_node.arg, collector.yield_stat_nodes[yield_node])
        except KeyError:
            return None, None

    def _handle_simple_function_all(self, node, pos_args):
        """Transform

        _result = all(x for L in LL for x in L)

        into

        for L in LL:
            for x in L:
                if not x:
                    _result = False
                    break
            else:
                continue
            break
        else:
            _result = True
        """
        return self._transform_any_all(node, pos_args, False)

    def _handle_simple_function_any(self, node, pos_args):
        """Transform

        _result = any(x for L in LL for x in L)

        into

        for L in LL:
            for x in L:
                if x:
                    _result = True
                    break
            else:
                continue
            break
        else:
            _result = False
        """
        return self._transform_any_all(node, pos_args, True)

    def _transform_any_all(self, node, pos_args, is_any):
        if len(pos_args) != 1:
            return node
        if not isinstance(pos_args[0], ExprNodes.GeneratorExpressionNode):
            return node
        gen_expr_node = pos_args[0]
        loop_node = gen_expr_node.loop
        yield_expression, yield_stat_node = self._find_single_yield_expression(loop_node)
        if yield_expression is None:
            return node

        if is_any:
            condition = yield_expression
        else:
            condition = ExprNodes.NotNode(yield_expression.pos, operand = yield_expression)

        result_ref = UtilNodes.ResultRefNode(pos=node.pos, type=PyrexTypes.c_bint_type)
        test_node = Nodes.IfStatNode(
            yield_expression.pos,
            else_clause = None,
            if_clauses = [ Nodes.IfClauseNode(
                yield_expression.pos,
                condition = condition,
                body = Nodes.StatListNode(
                    node.pos,
                    stats = [
                        Nodes.SingleAssignmentNode(
                            node.pos,
                            lhs = result_ref,
                            rhs = ExprNodes.BoolNode(yield_expression.pos, value = is_any,
                                                     constant_result = is_any)),
                        Nodes.BreakStatNode(node.pos)
                        ])) ]
            )
        loop = loop_node
        while isinstance(loop.body, Nodes.LoopNode):
            next_loop = loop.body
            loop.body = Nodes.StatListNode(loop.body.pos, stats = [
                loop.body,
                Nodes.BreakStatNode(yield_expression.pos)
                ])
            next_loop.else_clause = Nodes.ContinueStatNode(yield_expression.pos)
            loop = next_loop
        loop_node.else_clause = Nodes.SingleAssignmentNode(
            node.pos,
            lhs = result_ref,
            rhs = ExprNodes.BoolNode(yield_expression.pos, value = not is_any,
                                     constant_result = not is_any))

        Visitor.recursively_replace_node(loop_node, yield_stat_node, test_node)

        return ExprNodes.InlinedGeneratorExpressionNode(
            gen_expr_node.pos, loop = loop_node, result_node = result_ref,
            expr_scope = gen_expr_node.expr_scope, orig_func = is_any and 'any' or 'all')

    def _handle_simple_function_sorted(self, node, pos_args):
        """Transform sorted(genexpr) and sorted([listcomp]) into
        [listcomp].sort().  CPython just reads the iterable into a
        list and calls .sort() on it.  Expanding the iterable in a
        listcomp is still faster and the result can be sorted in
        place.
        """
        if len(pos_args) != 1:
            return node
        if isinstance(pos_args[0], ExprNodes.ComprehensionNode) \
               and pos_args[0].target.type is Builtin.list_type:
            listcomp_node = pos_args[0]
            loop_node = listcomp_node.loop
        elif isinstance(pos_args[0], ExprNodes.GeneratorExpressionNode):
            gen_expr_node = pos_args[0]
            loop_node = gen_expr_node.loop
            yield_expression, yield_stat_node = self._find_single_yield_expression(loop_node)
            if yield_expression is None:
                return node

            target = ExprNodes.ListNode(node.pos, args = [])
            append_node = ExprNodes.ComprehensionAppendNode(
                yield_expression.pos, expr = yield_expression,
                target = ExprNodes.CloneNode(target))

            Visitor.recursively_replace_node(loop_node, yield_stat_node, append_node)

            listcomp_node = ExprNodes.ComprehensionNode(
                gen_expr_node.pos, loop = loop_node, target = target,
                append = append_node, type = Builtin.list_type,
                expr_scope = gen_expr_node.expr_scope,
                has_local_scope = True)
        else:
            return node

        result_node = UtilNodes.ResultRefNode(
            pos = loop_node.pos, type = Builtin.list_type, may_hold_none=False)
        listcomp_assign_node = Nodes.SingleAssignmentNode(
            node.pos, lhs = result_node, rhs = listcomp_node, first = True)

        sort_method = ExprNodes.AttributeNode(
            node.pos, obj = result_node, attribute = EncodedString('sort'),
            # entry ? type ?
            needs_none_check = False)
        sort_node = Nodes.ExprStatNode(
            node.pos, expr = ExprNodes.SimpleCallNode(
                node.pos, function = sort_method, args = []))

        sort_node.analyse_declarations(self.current_env())

        return UtilNodes.TempResultFromStatNode(
            result_node,
            Nodes.StatListNode(node.pos, stats = [ listcomp_assign_node, sort_node ]))

    def _handle_simple_function_sum(self, node, pos_args):
        """Transform sum(genexpr) into an equivalent inlined aggregation loop.
        """
        if len(pos_args) not in (1,2):
            return node
        if not isinstance(pos_args[0], (ExprNodes.GeneratorExpressionNode,
                                        ExprNodes.ComprehensionNode)):
            return node
        gen_expr_node = pos_args[0]
        loop_node = gen_expr_node.loop

        if isinstance(gen_expr_node, ExprNodes.GeneratorExpressionNode):
            yield_expression, yield_stat_node = self._find_single_yield_expression(loop_node)
            if yield_expression is None:
                return node
        else: # ComprehensionNode
            yield_stat_node = gen_expr_node.append
            yield_expression = yield_stat_node.expr
            try:
                if not yield_expression.is_literal or not yield_expression.type.is_int:
                    return node
            except AttributeError:
                return node # in case we don't have a type yet
            # special case: old Py2 backwards compatible "sum([int_const for ...])"
            # can safely be unpacked into a genexpr

        if len(pos_args) == 1:
            start = ExprNodes.IntNode(node.pos, value='0', constant_result=0)
        else:
            start = pos_args[1]

        result_ref = UtilNodes.ResultRefNode(pos=node.pos, type=PyrexTypes.py_object_type)
        add_node = Nodes.SingleAssignmentNode(
            yield_expression.pos,
            lhs = result_ref,
            rhs = ExprNodes.binop_node(node.pos, '+', result_ref, yield_expression)
            )

        Visitor.recursively_replace_node(loop_node, yield_stat_node, add_node)

        exec_code = Nodes.StatListNode(
            node.pos,
            stats = [
                Nodes.SingleAssignmentNode(
                    start.pos,
                    lhs = UtilNodes.ResultRefNode(pos=node.pos, expression=result_ref),
                    rhs = start,
                    first = True),
                loop_node
                ])

        return ExprNodes.InlinedGeneratorExpressionNode(
            gen_expr_node.pos, loop = exec_code, result_node = result_ref,
            expr_scope = gen_expr_node.expr_scope, orig_func = 'sum',
            has_local_scope = gen_expr_node.has_local_scope)

    def _handle_simple_function_min(self, node, pos_args):
        return self._optimise_min_max(node, pos_args, '<')

    def _handle_simple_function_max(self, node, pos_args):
        return self._optimise_min_max(node, pos_args, '>')

    def _optimise_min_max(self, node, args, operator):
        """Replace min(a,b,...) and max(a,b,...) by explicit comparison code.
        """
        if len(args) <= 1:
            # leave this to Python
            return node

        cascaded_nodes = list(map(UtilNodes.ResultRefNode, args[1:]))

        last_result = args[0]
        for arg_node in cascaded_nodes:
            result_ref = UtilNodes.ResultRefNode(last_result)
            last_result = ExprNodes.CondExprNode(
                arg_node.pos,
                true_val = arg_node,
                false_val = result_ref,
                test = ExprNodes.PrimaryCmpNode(
                    arg_node.pos,
                    operand1 = arg_node,
                    operator = operator,
                    operand2 = result_ref,
                    )
                )
            last_result = UtilNodes.EvalWithTempExprNode(result_ref, last_result)

        for ref_node in cascaded_nodes[::-1]:
            last_result = UtilNodes.EvalWithTempExprNode(ref_node, last_result)

        return last_result

    def _DISABLED_handle_simple_function_tuple(self, node, pos_args):
        if not pos_args:
            return ExprNodes.TupleNode(node.pos, args=[], constant_result=())
        # This is a bit special - for iterables (including genexps),
        # Python actually overallocates and resizes a newly created
        # tuple incrementally while reading items, which we can't
        # easily do without explicit node support. Instead, we read
        # the items into a list and then copy them into a tuple of the
        # final size.  This takes up to twice as much memory, but will
        # have to do until we have real support for genexps.
        result = self._transform_list_set_genexpr(node, pos_args, ExprNodes.ListNode)
        if result is not node:
            return ExprNodes.AsTupleNode(node.pos, arg=result)
        return node

    def _handle_simple_function_list(self, node, pos_args):
        if not pos_args:
            return ExprNodes.ListNode(node.pos, args=[], constant_result=[])
        return self._transform_list_set_genexpr(node, pos_args, ExprNodes.ListNode)

    def _handle_simple_function_set(self, node, pos_args):
        if not pos_args:
            return ExprNodes.SetNode(node.pos, args=[], constant_result=set())
        return self._transform_list_set_genexpr(node, pos_args, ExprNodes.SetNode)

    def _transform_list_set_genexpr(self, node, pos_args, container_node_class):
        """Replace set(genexpr) and list(genexpr) by a literal comprehension.
        """
        if len(pos_args) > 1:
            return node
        if not isinstance(pos_args[0], ExprNodes.GeneratorExpressionNode):
            return node
        gen_expr_node = pos_args[0]
        loop_node = gen_expr_node.loop

        yield_expression, yield_stat_node = self._find_single_yield_expression(loop_node)
        if yield_expression is None:
            return node

        target_node = container_node_class(node.pos, args=[])
        append_node = ExprNodes.ComprehensionAppendNode(
            yield_expression.pos,
            expr = yield_expression,
            target = ExprNodes.CloneNode(target_node))

        Visitor.recursively_replace_node(loop_node, yield_stat_node, append_node)

        setcomp = ExprNodes.ComprehensionNode(
            node.pos,
            has_local_scope = True,
            expr_scope = gen_expr_node.expr_scope,
            loop = loop_node,
            append = append_node,
            target = target_node)
        append_node.target = setcomp
        return setcomp

    def _handle_simple_function_dict(self, node, pos_args):
        """Replace dict( (a,b) for ... ) by a literal { a:b for ... }.
        """
        if len(pos_args) == 0:
            return ExprNodes.DictNode(node.pos, key_value_pairs=[], constant_result={})
        if len(pos_args) > 1:
            return node
        if not isinstance(pos_args[0], ExprNodes.GeneratorExpressionNode):
            return node
        gen_expr_node = pos_args[0]
        loop_node = gen_expr_node.loop

        yield_expression, yield_stat_node = self._find_single_yield_expression(loop_node)
        if yield_expression is None:
            return node

        if not isinstance(yield_expression, ExprNodes.TupleNode):
            return node
        if len(yield_expression.args) != 2:
            return node

        target_node = ExprNodes.DictNode(node.pos, key_value_pairs=[])
        append_node = ExprNodes.DictComprehensionAppendNode(
            yield_expression.pos,
            key_expr = yield_expression.args[0],
            value_expr = yield_expression.args[1],
            target = ExprNodes.CloneNode(target_node))

        Visitor.recursively_replace_node(loop_node, yield_stat_node, append_node)

        dictcomp = ExprNodes.ComprehensionNode(
            node.pos,
            has_local_scope = True,
            expr_scope = gen_expr_node.expr_scope,
            loop = loop_node,
            append = append_node,
            target = target_node)
        append_node.target = dictcomp
        return dictcomp

    # specific handlers for general call nodes

    def _handle_general_function_dict(self, node, pos_args, kwargs):
        """Replace dict(a=b,c=d,...) by the underlying keyword dict
        construction which is done anyway.
        """
        if len(pos_args) > 0:
            return node
        if not isinstance(kwargs, ExprNodes.DictNode):
            return node
        return kwargs

class InlineDefNodeCalls(Visitor.CythonTransform):
    visit_Node = Visitor.VisitorTransform.recurse_to_children

    def visit_SimpleCallNode(self, node):
        self.visitchildren(node)
        if not self.current_directives.get('optimize.inline_defnode_calls'):
            return node
        function_name = node.function
        if not function_name.is_name:
            return node
        if (function_name.cf_state is None or
            not function_name.cf_state.is_single):
            return node
        function = function_name.cf_state.one().rhs
        if not isinstance(function, ExprNodes.PyCFunctionNode):
            return node
        inlined = ExprNodes.InlinedDefNodeCallNode(
            node.pos, function_name=function_name,
            function=function, args=node.args)
        if inlined.can_be_inlined():
            return inlined
        return node


class OptimizeBuiltinCalls(Visitor.EnvTransform):
    """Optimize some common methods calls and instantiation patterns
    for builtin types *after* the type analysis phase.

    Running after type analysis, this transform can only perform
    function replacements that do not alter the function return type
    in a way that was not anticipated by the type analysis.
    """
    # only intercept on call nodes
    visit_Node = Visitor.VisitorTransform.recurse_to_children

    def visit_GeneralCallNode(self, node):
        self.visitchildren(node)
        function = node.function
        if not function.type.is_pyobject:
            return node
        arg_tuple = node.positional_args
        if not isinstance(arg_tuple, ExprNodes.TupleNode):
            return node
        keyword_args = node.keyword_args
        if keyword_args and not isinstance(keyword_args, ExprNodes.DictNode):
            # can't handle **kwargs
            return node
        args = arg_tuple.args
        return self._dispatch_to_handler(
            node, function, args, keyword_args)

    def visit_SimpleCallNode(self, node):
        self.visitchildren(node)
        function = node.function
        if function.type.is_pyobject:
            arg_tuple = node.arg_tuple
            if not isinstance(arg_tuple, ExprNodes.TupleNode):
                return node
            args = arg_tuple.args
        else:
            args = node.args
        return self._dispatch_to_handler(
            node, function, args)

    ### cleanup to avoid redundant coercions to/from Python types

    def _visit_PyTypeTestNode(self, node):
        # disabled - appears to break assignments in some cases, and
        # also drops a None check, which might still be required
        """Flatten redundant type checks after tree changes.
        """
        old_arg = node.arg
        self.visitchildren(node)
        if old_arg is node.arg or node.arg.type != node.type:
            return node
        return node.arg

    def _visit_TypecastNode(self, node):
        # disabled - the user may have had a reason to put a type
        # cast, even if it looks redundant to Cython
        """
        Drop redundant type casts.
        """
        self.visitchildren(node)
        if node.type == node.operand.type:
            return node.operand
        return node

    def visit_ExprStatNode(self, node):
        """
        Drop useless coercions.
        """
        self.visitchildren(node)
        if isinstance(node.expr, ExprNodes.CoerceToPyTypeNode):
            node.expr = node.expr.arg
        return node

    def visit_CoerceToBooleanNode(self, node):
        """Drop redundant conversion nodes after tree changes.
        """
        self.visitchildren(node)
        arg = node.arg
        if isinstance(arg, ExprNodes.PyTypeTestNode):
            arg = arg.arg
        if isinstance(arg, ExprNodes.CoerceToPyTypeNode):
            if arg.type in (PyrexTypes.py_object_type, Builtin.bool_type):
                return arg.arg.coerce_to_boolean(self.current_env())
        return node

    def visit_CoerceFromPyTypeNode(self, node):
        """Drop redundant conversion nodes after tree changes.

        Also, optimise away calls to Python's builtin int() and
        float() if the result is going to be coerced back into a C
        type anyway.
        """
        self.visitchildren(node)
        arg = node.arg
        if not arg.type.is_pyobject:
            # no Python conversion left at all, just do a C coercion instead
            if node.type == arg.type:
                return arg
            else:
                return arg.coerce_to(node.type, self.current_env())
        if isinstance(arg, ExprNodes.PyTypeTestNode):
            arg = arg.arg
        if isinstance(arg, ExprNodes.CoerceToPyTypeNode):
            if arg.type is PyrexTypes.py_object_type:
                if node.type.assignable_from(arg.arg.type):
                    # completely redundant C->Py->C coercion
                    return arg.arg.coerce_to(node.type, self.current_env())
        if isinstance(arg, ExprNodes.SimpleCallNode):
            if node.type.is_int or node.type.is_float:
                return self._optimise_numeric_cast_call(node, arg)
        elif isinstance(arg, ExprNodes.IndexNode) and not arg.is_buffer_access:
            index_node = arg.index
            if isinstance(index_node, ExprNodes.CoerceToPyTypeNode):
                index_node = index_node.arg
            if index_node.type.is_int:
                return self._optimise_int_indexing(node, arg, index_node)
        return node

    PyBytes_GetItemInt_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_char_type, [
            PyrexTypes.CFuncTypeArg("bytes", Builtin.bytes_type, None),
            PyrexTypes.CFuncTypeArg("index", PyrexTypes.c_py_ssize_t_type, None),
            PyrexTypes.CFuncTypeArg("check_bounds", PyrexTypes.c_int_type, None),
            ],
        exception_value = "((char)-1)",
        exception_check = True)

    def _optimise_int_indexing(self, coerce_node, arg, index_node):
        env = self.current_env()
        bound_check_bool = env.directives['boundscheck'] and 1 or 0
        if arg.base.type is Builtin.bytes_type:
            if coerce_node.type in (PyrexTypes.c_char_type, PyrexTypes.c_uchar_type):
                # bytes[index] -> char
                bound_check_node = ExprNodes.IntNode(
                    coerce_node.pos, value=str(bound_check_bool),
                    constant_result=bound_check_bool)
                node = ExprNodes.PythonCapiCallNode(
                    coerce_node.pos, "__Pyx_PyBytes_GetItemInt",
                    self.PyBytes_GetItemInt_func_type,
                    args = [
                        arg.base.as_none_safe_node("'NoneType' object is not subscriptable"),
                        index_node.coerce_to(PyrexTypes.c_py_ssize_t_type, env),
                        bound_check_node,
                        ],
                    is_temp = True,
                    utility_code=load_c_utility('bytes_index'))
                if coerce_node.type is not PyrexTypes.c_char_type:
                    node = node.coerce_to(coerce_node.type, env)
                return node
        return coerce_node

    def _optimise_numeric_cast_call(self, node, arg):
        function = arg.function
        if not isinstance(function, ExprNodes.NameNode) \
               or not function.type.is_builtin_type \
               or not isinstance(arg.arg_tuple, ExprNodes.TupleNode):
            return node
        args = arg.arg_tuple.args
        if len(args) != 1:
            return node
        func_arg = args[0]
        if isinstance(func_arg, ExprNodes.CoerceToPyTypeNode):
            func_arg = func_arg.arg
        elif func_arg.type.is_pyobject:
            # play safe: Python conversion might work on all sorts of things
            return node
        if function.name == 'int':
            if func_arg.type.is_int or node.type.is_int:
                if func_arg.type == node.type:
                    return func_arg
                elif node.type.assignable_from(func_arg.type) or func_arg.type.is_float:
                    return ExprNodes.TypecastNode(
                        node.pos, operand=func_arg, type=node.type)
        elif function.name == 'float':
            if func_arg.type.is_float or node.type.is_float:
                if func_arg.type == node.type:
                    return func_arg
                elif node.type.assignable_from(func_arg.type) or func_arg.type.is_float:
                    return ExprNodes.TypecastNode(
                        node.pos, operand=func_arg, type=node.type)
        return node

    ### dispatch to specific optimisers

    def _find_handler(self, match_name, has_kwargs):
        call_type = has_kwargs and 'general' or 'simple'
        handler = getattr(self, '_handle_%s_%s' % (call_type, match_name), None)
        if handler is None:
            handler = getattr(self, '_handle_any_%s' % match_name, None)
        return handler

    def _dispatch_to_handler(self, node, function, arg_list, kwargs=None):
        if function.is_name:
            # we only consider functions that are either builtin
            # Python functions or builtins that were already replaced
            # into a C function call (defined in the builtin scope)
            if not function.entry:
                return node
            is_builtin = function.entry.is_builtin or \
                         function.entry is self.current_env().builtin_scope().lookup_here(function.name)
            if not is_builtin:
                return node
            function_handler = self._find_handler(
                "function_%s" % function.name, kwargs)
            if function_handler is None:
                return node
            if kwargs:
                return function_handler(node, arg_list, kwargs)
            else:
                return function_handler(node, arg_list)
        elif function.is_attribute and function.type.is_pyobject:
            attr_name = function.attribute
            self_arg = function.obj
            obj_type = self_arg.type
            is_unbound_method = False
            if obj_type.is_builtin_type:
                if obj_type is Builtin.type_type and arg_list and \
                         arg_list[0].type.is_pyobject:
                    # calling an unbound method like 'list.append(L,x)'
                    # (ignoring 'type.mro()' here ...)
                    type_name = function.obj.name
                    self_arg = None
                    is_unbound_method = True
                else:
                    type_name = obj_type.name
            else:
                type_name = "object" # safety measure
            method_handler = self._find_handler(
                "method_%s_%s" % (type_name, attr_name), kwargs)
            if method_handler is None:
                if attr_name in TypeSlots.method_name_to_slot \
                       or attr_name == '__new__':
                    method_handler = self._find_handler(
                        "slot%s" % attr_name, kwargs)
                if method_handler is None:
                    return node
            if self_arg is not None:
                arg_list = [self_arg] + list(arg_list)
            if kwargs:
                return method_handler(node, arg_list, kwargs, is_unbound_method)
            else:
                return method_handler(node, arg_list, is_unbound_method)
        else:
            return node

    def _error_wrong_arg_count(self, function_name, node, args, expected=None):
        if not expected: # None or 0
            arg_str = ''
        elif isinstance(expected, basestring) or expected > 1:
            arg_str = '...'
        elif expected == 1:
            arg_str = 'x'
        else:
            arg_str = ''
        if expected is not None:
            expected_str = 'expected %s, ' % expected
        else:
            expected_str = ''
        error(node.pos, "%s(%s) called with wrong number of args, %sfound %d" % (
            function_name, arg_str, expected_str, len(args)))

    ### builtin types

    PyDict_Copy_func_type = PyrexTypes.CFuncType(
        Builtin.dict_type, [
            PyrexTypes.CFuncTypeArg("dict", Builtin.dict_type, None)
            ])

    def _handle_simple_function_dict(self, node, pos_args):
        """Replace dict(some_dict) by PyDict_Copy(some_dict).
        """
        if len(pos_args) != 1:
            return node
        arg = pos_args[0]
        if arg.type is Builtin.dict_type:
            arg = arg.as_none_safe_node("'NoneType' is not iterable")
            return ExprNodes.PythonCapiCallNode(
                node.pos, "PyDict_Copy", self.PyDict_Copy_func_type,
                args = [arg],
                is_temp = node.is_temp
                )
        return node

    PyList_AsTuple_func_type = PyrexTypes.CFuncType(
        Builtin.tuple_type, [
            PyrexTypes.CFuncTypeArg("list", Builtin.list_type, None)
            ])

    def _handle_simple_function_tuple(self, node, pos_args):
        """Replace tuple([...]) by a call to PyList_AsTuple.
        """
        if len(pos_args) != 1:
            return node
        list_arg = pos_args[0]
        if list_arg.type is not Builtin.list_type:
            return node
        if not isinstance(list_arg, (ExprNodes.ComprehensionNode,
                                     ExprNodes.ListNode)):
            pos_args[0] = list_arg.as_none_safe_node(
                "'NoneType' object is not iterable")

        return ExprNodes.PythonCapiCallNode(
            node.pos, "PyList_AsTuple", self.PyList_AsTuple_func_type,
            args = pos_args,
            is_temp = node.is_temp
            )

    PyObject_AsDouble_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_double_type, [
            PyrexTypes.CFuncTypeArg("obj", PyrexTypes.py_object_type, None),
            ],
        exception_value = "((double)-1)",
        exception_check = True)

    def _handle_simple_function_set(self, node, pos_args):
        if len(pos_args) == 1 and isinstance(pos_args[0], (ExprNodes.ListNode,
                                                           ExprNodes.TupleNode)):
            # We can optimise set([x,y,z]) safely into a set literal,
            # but only if we create all items before adding them -
            # adding an item may raise an exception if it is not
            # hashable, but creating the later items may have
            # side-effects.
            args = []
            temps = []
            for arg in pos_args[0].args:
                if not arg.is_simple():
                    arg = UtilNodes.LetRefNode(arg)
                    temps.append(arg)
                args.append(arg)
            result = ExprNodes.SetNode(node.pos, is_temp=1, args=args)
            for temp in temps[::-1]:
                result = UtilNodes.EvalWithTempExprNode(temp, result)
            return result
        return node

    def _handle_simple_function_float(self, node, pos_args):
        """Transform float() into either a C type cast or a faster C
        function call.
        """
        # Note: this requires the float() function to be typed as
        # returning a C 'double'
        if len(pos_args) == 0:
            return ExprNodes.FloatNode(
                node, value="0.0", constant_result=0.0
                ).coerce_to(Builtin.float_type, self.current_env())
        elif len(pos_args) != 1:
            self._error_wrong_arg_count('float', node, pos_args, '0 or 1')
            return node
        func_arg = pos_args[0]
        if isinstance(func_arg, ExprNodes.CoerceToPyTypeNode):
            func_arg = func_arg.arg
        if func_arg.type is PyrexTypes.c_double_type:
            return func_arg
        elif node.type.assignable_from(func_arg.type) or func_arg.type.is_numeric:
            return ExprNodes.TypecastNode(
                node.pos, operand=func_arg, type=node.type)
        return ExprNodes.PythonCapiCallNode(
            node.pos, "__Pyx_PyObject_AsDouble",
            self.PyObject_AsDouble_func_type,
            args = pos_args,
            is_temp = node.is_temp,
            utility_code = load_c_utility('pyobject_as_double'),
            py_name = "float")

    def _handle_simple_function_bool(self, node, pos_args):
        """Transform bool(x) into a type coercion to a boolean.
        """
        if len(pos_args) == 0:
            return ExprNodes.BoolNode(
                node.pos, value=False, constant_result=False
                ).coerce_to(Builtin.bool_type, self.current_env())
        elif len(pos_args) != 1:
            self._error_wrong_arg_count('bool', node, pos_args, '0 or 1')
            return node
        else:
            # => !!<bint>(x)  to make sure it's exactly 0 or 1
            operand = pos_args[0].coerce_to_boolean(self.current_env())
            operand = ExprNodes.NotNode(node.pos, operand = operand)
            operand = ExprNodes.NotNode(node.pos, operand = operand)
            # coerce back to Python object as that's the result we are expecting
            return operand.coerce_to_pyobject(self.current_env())

    ### builtin functions

    Pyx_strlen_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_size_t_type, [
            PyrexTypes.CFuncTypeArg("bytes", PyrexTypes.c_char_ptr_type, None)
            ])

    PyObject_Size_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_py_ssize_t_type, [
            PyrexTypes.CFuncTypeArg("obj", PyrexTypes.py_object_type, None)
            ])

    _map_to_capi_len_function = {
        Builtin.unicode_type   : "__Pyx_PyUnicode_GET_LENGTH",
        Builtin.bytes_type     : "PyBytes_GET_SIZE",
        Builtin.list_type      : "PyList_GET_SIZE",
        Builtin.tuple_type     : "PyTuple_GET_SIZE",
        Builtin.dict_type      : "PyDict_Size",
        Builtin.set_type       : "PySet_Size",
        Builtin.frozenset_type : "PySet_Size",
        }.get

    def _handle_simple_function_len(self, node, pos_args):
        """Replace len(char*) by the equivalent call to strlen() and
        len(known_builtin_type) by an equivalent C-API call.
        """
        if len(pos_args) != 1:
            self._error_wrong_arg_count('len', node, pos_args, 1)
            return node
        arg = pos_args[0]
        if isinstance(arg, ExprNodes.CoerceToPyTypeNode):
            arg = arg.arg
        if arg.type.is_string:
            new_node = ExprNodes.PythonCapiCallNode(
                node.pos, "strlen", self.Pyx_strlen_func_type,
                args = [arg],
                is_temp = node.is_temp,
                utility_code = UtilityCode.load_cached("IncludeStringH", "StringTools.c"))
        elif arg.type.is_pyobject:
            cfunc_name = self._map_to_capi_len_function(arg.type)
            if cfunc_name is None:
                return node
            arg = arg.as_none_safe_node(
                "object of type 'NoneType' has no len()")
            new_node = ExprNodes.PythonCapiCallNode(
                node.pos, cfunc_name, self.PyObject_Size_func_type,
                args = [arg],
                is_temp = node.is_temp)
        elif arg.type.is_unicode_char:
            return ExprNodes.IntNode(node.pos, value='1', constant_result=1,
                                     type=node.type)
        else:
            return node
        if node.type not in (PyrexTypes.c_size_t_type, PyrexTypes.c_py_ssize_t_type):
            new_node = new_node.coerce_to(node.type, self.current_env())
        return new_node

    Pyx_Type_func_type = PyrexTypes.CFuncType(
        Builtin.type_type, [
            PyrexTypes.CFuncTypeArg("object", PyrexTypes.py_object_type, None)
            ])

    def _handle_simple_function_type(self, node, pos_args):
        """Replace type(o) by a macro call to Py_TYPE(o).
        """
        if len(pos_args) != 1:
            return node
        node = ExprNodes.PythonCapiCallNode(
            node.pos, "Py_TYPE", self.Pyx_Type_func_type,
            args = pos_args,
            is_temp = False)
        return ExprNodes.CastNode(node, PyrexTypes.py_object_type)

    Py_type_check_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_bint_type, [
            PyrexTypes.CFuncTypeArg("arg", PyrexTypes.py_object_type, None)
            ])

    def _handle_simple_function_isinstance(self, node, pos_args):
        """Replace isinstance() checks against builtin types by the
        corresponding C-API call.
        """
        if len(pos_args) != 2:
            return node
        arg, types = pos_args
        temp = None
        if isinstance(types, ExprNodes.TupleNode):
            types = types.args
            arg = temp = UtilNodes.ResultRefNode(arg)
        elif types.type is Builtin.type_type:
            types = [types]
        else:
            return node

        tests = []
        test_nodes = []
        env = self.current_env()
        for test_type_node in types:
            builtin_type = None
            if isinstance(test_type_node, ExprNodes.NameNode):
                if test_type_node.entry:
                    entry = env.lookup(test_type_node.entry.name)
                    if entry and entry.type and entry.type.is_builtin_type:
                        builtin_type = entry.type
            if builtin_type and builtin_type is not Builtin.type_type:
                type_check_function = entry.type.type_check_function(exact=False)
                if type_check_function in tests:
                    continue
                tests.append(type_check_function)
                type_check_args = [arg]
            elif test_type_node.type is Builtin.type_type:
                type_check_function = '__Pyx_TypeCheck'
                type_check_args = [arg, test_type_node]
            else:
                return node
            test_nodes.append(
                ExprNodes.PythonCapiCallNode(
                    test_type_node.pos, type_check_function, self.Py_type_check_func_type,
                    args = type_check_args,
                    is_temp = True,
                    ))

        def join_with_or(a,b, make_binop_node=ExprNodes.binop_node):
            or_node = make_binop_node(node.pos, 'or', a, b)
            or_node.type = PyrexTypes.c_bint_type
            or_node.is_temp = True
            return or_node

        test_node = reduce(join_with_or, test_nodes).coerce_to(node.type, env)
        if temp is not None:
            test_node = UtilNodes.EvalWithTempExprNode(temp, test_node)
        return test_node

    def _handle_simple_function_ord(self, node, pos_args):
        """Unpack ord(Py_UNICODE) and ord('X').
        """
        if len(pos_args) != 1:
            return node
        arg = pos_args[0]
        if isinstance(arg, ExprNodes.CoerceToPyTypeNode):
            if arg.arg.type.is_unicode_char:
                return ExprNodes.TypecastNode(
                    arg.pos, operand=arg.arg, type=PyrexTypes.c_int_type
                    ).coerce_to(node.type, self.current_env())
        elif isinstance(arg, ExprNodes.UnicodeNode):
            if len(arg.value) == 1:
                return ExprNodes.IntNode(
                    ord(arg.value), type=PyrexTypes.c_int_type,
                    value=str(ord(arg.value)),
                    constant_result=ord(arg.value)
                    ).coerce_to(node.type, self.current_env())
        elif isinstance(arg, ExprNodes.StringNode):
            if arg.unicode_value and len(arg.unicode_value) == 1 \
                   and ord(arg.unicode_value) <= 255: # Py2/3 portability
                return ExprNodes.IntNode(
                    ord(arg.unicode_value), type=PyrexTypes.c_int_type,
                    value=str(ord(arg.unicode_value)),
                    constant_result=ord(arg.unicode_value)
                    ).coerce_to(node.type, self.current_env())
        return node

    ### special methods

    Pyx_tp_new_func_type = PyrexTypes.CFuncType(
        PyrexTypes.py_object_type, [
            PyrexTypes.CFuncTypeArg("type", Builtin.type_type, None)
            ])

    def _handle_simple_slot__new__(self, node, args, is_unbound_method):
        """Replace 'exttype.__new__(exttype)' by a call to exttype->tp_new()
        """
        obj = node.function.obj
        if not is_unbound_method or len(args) != 1:
            return node
        type_arg = args[0]
        if not obj.is_name or not type_arg.is_name:
            # play safe
            return node
        if obj.type != Builtin.type_type or type_arg.type != Builtin.type_type:
            # not a known type, play safe
            return node
        if not type_arg.type_entry or not obj.type_entry:
            if obj.name != type_arg.name:
                return node
            # otherwise, we know it's a type and we know it's the same
            # type for both - that should do
        elif type_arg.type_entry != obj.type_entry:
            # different types - may or may not lead to an error at runtime
            return node

        # FIXME: we could potentially look up the actual tp_new C
        # method of the extension type and call that instead of the
        # generic slot. That would also allow us to pass parameters
        # efficiently.

        if not type_arg.type_entry:
            # arbitrary variable, needs a None check for safety
            type_arg = type_arg.as_none_safe_node(
                "object.__new__(X): X is not a type object (NoneType)")

        return ExprNodes.PythonCapiCallNode(
            node.pos, "__Pyx_tp_new", self.Pyx_tp_new_func_type,
            args = [type_arg],
            utility_code = tpnew_utility_code,
            is_temp = node.is_temp
            )

    ### methods of builtin types

    PyDict_Clear_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_void_type, [
            PyrexTypes.CFuncTypeArg("dict", Builtin.dict_type, None)
            ])

    PyDict_Clear_Retval_func_type = PyrexTypes.CFuncType(
        PyrexTypes.py_object_type, [
            PyrexTypes.CFuncTypeArg("dict", Builtin.dict_type, None)
            ])

    def _handle_simple_method_dict_clear(self, node, args, is_unbound_method):
        """Optimise dict.clear() differently, depending on the use (or
        non-use) of the return value.
        """
        if len(args) != 1:
            return node
        if node.result_is_used:
            return self._substitute_method_call(
                node, "__Pyx_PyDict_Clear", self.PyDict_Clear_Retval_func_type,
                'clear', is_unbound_method, args,
                may_return_none=True, is_temp=True,
                utility_code=load_c_utility('py_dict_clear')
                ).coerce_to(node.type, self.current_env)
        else:
            return self._substitute_method_call(
                node, "PyDict_Clear", self.PyDict_Clear_func_type,
                'clear', is_unbound_method, args, is_temp=False)

    PyObject_Append_func_type = PyrexTypes.CFuncType(
        PyrexTypes.py_object_type, [
            PyrexTypes.CFuncTypeArg("list", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("item", PyrexTypes.py_object_type, None),
            ])

    def _handle_simple_method_object_append(self, node, args, is_unbound_method):
        """Optimistic optimisation as X.append() is almost always
        referring to a list.
        """
        if len(args) != 2:
            return node

        return ExprNodes.PythonCapiCallNode(
            node.pos, "__Pyx_PyObject_Append", self.PyObject_Append_func_type,
            args = args,
            may_return_none = True,
            is_temp = node.is_temp,
            utility_code = load_c_utility('append')
            )

    PyObject_Pop_func_type = PyrexTypes.CFuncType(
        PyrexTypes.py_object_type, [
            PyrexTypes.CFuncTypeArg("list", PyrexTypes.py_object_type, None),
            ])

    PyObject_PopIndex_func_type = PyrexTypes.CFuncType(
        PyrexTypes.py_object_type, [
            PyrexTypes.CFuncTypeArg("list", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("index", PyrexTypes.c_long_type, None),
            ])

    def _handle_simple_method_object_pop(self, node, args, is_unbound_method):
        """Optimistic optimisation as X.pop([n]) is almost always
        referring to a list.
        """
        if len(args) == 1:
            return ExprNodes.PythonCapiCallNode(
                node.pos, "__Pyx_PyObject_Pop", self.PyObject_Pop_func_type,
                args = args,
                may_return_none = True,
                is_temp = node.is_temp,
                utility_code = load_c_utility('pop')
                )
        elif len(args) == 2:
            index = args[1]
            if isinstance(index, ExprNodes.CoerceToPyTypeNode):
                index = index.arg
            if isinstance(index, ExprNodes.IntNode):
                index = index.coerce_to(PyrexTypes.c_py_ssize_t_type, None)
            if index.type.is_int:
                widest = PyrexTypes.widest_numeric_type(
                    index.type, PyrexTypes.c_py_ssize_t_type)
                if widest == PyrexTypes.c_py_ssize_t_type:
                    args[1] = index
                    return ExprNodes.PythonCapiCallNode(
                        node.pos, "__Pyx_PyObject_PopIndex",
                        self.PyObject_PopIndex_func_type,
                        args = args,
                        may_return_none = True,
                        is_temp = node.is_temp,
                        utility_code = load_c_utility("pop_index")
                        )

        return node

    _handle_simple_method_list_pop = _handle_simple_method_object_pop

    single_param_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_returncode_type, [
            PyrexTypes.CFuncTypeArg("obj", PyrexTypes.py_object_type, None),
            ],
        exception_value = "-1")

    def _handle_simple_method_list_sort(self, node, args, is_unbound_method):
        """Call PyList_Sort() instead of the 0-argument l.sort().
        """
        if len(args) != 1:
            return node
        return self._substitute_method_call(
            node, "PyList_Sort", self.single_param_func_type,
            'sort', is_unbound_method, args).coerce_to(node.type, self.current_env)

    Pyx_PyDict_GetItem_func_type = PyrexTypes.CFuncType(
        PyrexTypes.py_object_type, [
            PyrexTypes.CFuncTypeArg("dict", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("key", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("default", PyrexTypes.py_object_type, None),
            ])

    def _handle_simple_method_dict_get(self, node, args, is_unbound_method):
        """Replace dict.get() by a call to PyDict_GetItem().
        """
        if len(args) == 2:
            args.append(ExprNodes.NoneNode(node.pos))
        elif len(args) != 3:
            self._error_wrong_arg_count('dict.get', node, args, "2 or 3")
            return node

        return self._substitute_method_call(
            node, "__Pyx_PyDict_GetItemDefault", self.Pyx_PyDict_GetItem_func_type,
            'get', is_unbound_method, args,
            may_return_none = True,
            utility_code = load_c_utility("dict_getitem_default"))

    Pyx_PyDict_SetDefault_func_type = PyrexTypes.CFuncType(
        PyrexTypes.py_object_type, [
            PyrexTypes.CFuncTypeArg("dict", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("key", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("default", PyrexTypes.py_object_type, None),
            ])

    def _handle_simple_method_dict_setdefault(self, node, args, is_unbound_method):
        """Replace dict.setdefault() by calls to PyDict_GetItem() and PyDict_SetItem().
        """
        if len(args) == 2:
            args.append(ExprNodes.NoneNode(node.pos))
        elif len(args) != 3:
            self._error_wrong_arg_count('dict.setdefault', node, args, "2 or 3")
            return node

        return self._substitute_method_call(
            node, "__Pyx_PyDict_SetDefault", self.Pyx_PyDict_SetDefault_func_type,
            'setdefault', is_unbound_method, args,
            may_return_none = True,
            utility_code = load_c_utility('dict_setdefault'))


    ### unicode type methods

    PyUnicode_uchar_predicate_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_bint_type, [
            PyrexTypes.CFuncTypeArg("uchar", PyrexTypes.c_py_ucs4_type, None),
            ])

    def _inject_unicode_predicate(self, node, args, is_unbound_method):
        if is_unbound_method or len(args) != 1:
            return node
        ustring = args[0]
        if not isinstance(ustring, ExprNodes.CoerceToPyTypeNode) or \
               not ustring.arg.type.is_unicode_char:
            return node
        uchar = ustring.arg
        method_name = node.function.attribute
        if method_name == 'istitle':
            # istitle() doesn't directly map to Py_UNICODE_ISTITLE()
            utility_code = load_c_utility("py_unicode_istitle")
            function_name = '__Pyx_Py_UNICODE_ISTITLE'
        else:
            utility_code = None
            function_name = 'Py_UNICODE_%s' % method_name.upper()
        func_call = self._substitute_method_call(
            node, function_name, self.PyUnicode_uchar_predicate_func_type,
            method_name, is_unbound_method, [uchar],
            utility_code = utility_code)
        if node.type.is_pyobject:
            func_call = func_call.coerce_to_pyobject(self.current_env)
        return func_call

    _handle_simple_method_unicode_isalnum   = _inject_unicode_predicate
    _handle_simple_method_unicode_isalpha   = _inject_unicode_predicate
    _handle_simple_method_unicode_isdecimal = _inject_unicode_predicate
    _handle_simple_method_unicode_isdigit   = _inject_unicode_predicate
    _handle_simple_method_unicode_islower   = _inject_unicode_predicate
    _handle_simple_method_unicode_isnumeric = _inject_unicode_predicate
    _handle_simple_method_unicode_isspace   = _inject_unicode_predicate
    _handle_simple_method_unicode_istitle   = _inject_unicode_predicate
    _handle_simple_method_unicode_isupper   = _inject_unicode_predicate

    PyUnicode_uchar_conversion_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_py_ucs4_type, [
            PyrexTypes.CFuncTypeArg("uchar", PyrexTypes.c_py_ucs4_type, None),
            ])

    def _inject_unicode_character_conversion(self, node, args, is_unbound_method):
        if is_unbound_method or len(args) != 1:
            return node
        ustring = args[0]
        if not isinstance(ustring, ExprNodes.CoerceToPyTypeNode) or \
               not ustring.arg.type.is_unicode_char:
            return node
        uchar = ustring.arg
        method_name = node.function.attribute
        function_name = 'Py_UNICODE_TO%s' % method_name.upper()
        func_call = self._substitute_method_call(
            node, function_name, self.PyUnicode_uchar_conversion_func_type,
            method_name, is_unbound_method, [uchar])
        if node.type.is_pyobject:
            func_call = func_call.coerce_to_pyobject(self.current_env)
        return func_call

    _handle_simple_method_unicode_lower = _inject_unicode_character_conversion
    _handle_simple_method_unicode_upper = _inject_unicode_character_conversion
    _handle_simple_method_unicode_title = _inject_unicode_character_conversion

    PyUnicode_Splitlines_func_type = PyrexTypes.CFuncType(
        Builtin.list_type, [
            PyrexTypes.CFuncTypeArg("str", Builtin.unicode_type, None),
            PyrexTypes.CFuncTypeArg("keepends", PyrexTypes.c_bint_type, None),
            ])

    def _handle_simple_method_unicode_splitlines(self, node, args, is_unbound_method):
        """Replace unicode.splitlines(...) by a direct call to the
        corresponding C-API function.
        """
        if len(args) not in (1,2):
            self._error_wrong_arg_count('unicode.splitlines', node, args, "1 or 2")
            return node
        self._inject_bint_default_argument(node, args, 1, False)

        return self._substitute_method_call(
            node, "PyUnicode_Splitlines", self.PyUnicode_Splitlines_func_type,
            'splitlines', is_unbound_method, args)

    PyUnicode_Split_func_type = PyrexTypes.CFuncType(
        Builtin.list_type, [
            PyrexTypes.CFuncTypeArg("str", Builtin.unicode_type, None),
            PyrexTypes.CFuncTypeArg("sep", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("maxsplit", PyrexTypes.c_py_ssize_t_type, None),
            ]
        )

    def _handle_simple_method_unicode_split(self, node, args, is_unbound_method):
        """Replace unicode.split(...) by a direct call to the
        corresponding C-API function.
        """
        if len(args) not in (1,2,3):
            self._error_wrong_arg_count('unicode.split', node, args, "1-3")
            return node
        if len(args) < 2:
            args.append(ExprNodes.NullNode(node.pos))
        self._inject_int_default_argument(
            node, args, 2, PyrexTypes.c_py_ssize_t_type, "-1")

        return self._substitute_method_call(
            node, "PyUnicode_Split", self.PyUnicode_Split_func_type,
            'split', is_unbound_method, args)

    PyString_Tailmatch_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_bint_type, [
            PyrexTypes.CFuncTypeArg("str", PyrexTypes.py_object_type, None),  # bytes/str/unicode
            PyrexTypes.CFuncTypeArg("substring", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("start", PyrexTypes.c_py_ssize_t_type, None),
            PyrexTypes.CFuncTypeArg("end", PyrexTypes.c_py_ssize_t_type, None),
            PyrexTypes.CFuncTypeArg("direction", PyrexTypes.c_int_type, None),
            ],
        exception_value = '-1')

    def _handle_simple_method_unicode_endswith(self, node, args, is_unbound_method):
        return self._inject_tailmatch(
            node, args, is_unbound_method, 'unicode', 'endswith',
            unicode_tailmatch_utility_code, +1)

    def _handle_simple_method_unicode_startswith(self, node, args, is_unbound_method):
        return self._inject_tailmatch(
            node, args, is_unbound_method, 'unicode', 'startswith',
            unicode_tailmatch_utility_code, -1)

    def _inject_tailmatch(self, node, args, is_unbound_method, type_name,
                          method_name, utility_code, direction):
        """Replace unicode.startswith(...) and unicode.endswith(...)
        by a direct call to the corresponding C-API function.
        """
        if len(args) not in (2,3,4):
            self._error_wrong_arg_count('%s.%s' % (type_name, method_name), node, args, "2-4")
            return node
        self._inject_int_default_argument(
            node, args, 2, PyrexTypes.c_py_ssize_t_type, "0")
        self._inject_int_default_argument(
            node, args, 3, PyrexTypes.c_py_ssize_t_type, "PY_SSIZE_T_MAX")
        args.append(ExprNodes.IntNode(
            node.pos, value=str(direction), type=PyrexTypes.c_int_type))

        method_call = self._substitute_method_call(
            node, "__Pyx_Py%s_Tailmatch" % type_name.capitalize(),
            self.PyString_Tailmatch_func_type,
            method_name, is_unbound_method, args,
            utility_code = utility_code)
        return method_call.coerce_to(Builtin.bool_type, self.current_env())

    PyUnicode_Find_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_py_ssize_t_type, [
            PyrexTypes.CFuncTypeArg("str", Builtin.unicode_type, None),
            PyrexTypes.CFuncTypeArg("substring", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("start", PyrexTypes.c_py_ssize_t_type, None),
            PyrexTypes.CFuncTypeArg("end", PyrexTypes.c_py_ssize_t_type, None),
            PyrexTypes.CFuncTypeArg("direction", PyrexTypes.c_int_type, None),
            ],
        exception_value = '-2')

    def _handle_simple_method_unicode_find(self, node, args, is_unbound_method):
        return self._inject_unicode_find(
            node, args, is_unbound_method, 'find', +1)

    def _handle_simple_method_unicode_rfind(self, node, args, is_unbound_method):
        return self._inject_unicode_find(
            node, args, is_unbound_method, 'rfind', -1)

    def _inject_unicode_find(self, node, args, is_unbound_method,
                             method_name, direction):
        """Replace unicode.find(...) and unicode.rfind(...) by a
        direct call to the corresponding C-API function.
        """
        if len(args) not in (2,3,4):
            self._error_wrong_arg_count('unicode.%s' % method_name, node, args, "2-4")
            return node
        self._inject_int_default_argument(
            node, args, 2, PyrexTypes.c_py_ssize_t_type, "0")
        self._inject_int_default_argument(
            node, args, 3, PyrexTypes.c_py_ssize_t_type, "PY_SSIZE_T_MAX")
        args.append(ExprNodes.IntNode(
            node.pos, value=str(direction), type=PyrexTypes.c_int_type))

        method_call = self._substitute_method_call(
            node, "PyUnicode_Find", self.PyUnicode_Find_func_type,
            method_name, is_unbound_method, args)
        return method_call.coerce_to_pyobject(self.current_env())

    PyUnicode_Count_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_py_ssize_t_type, [
            PyrexTypes.CFuncTypeArg("str", Builtin.unicode_type, None),
            PyrexTypes.CFuncTypeArg("substring", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("start", PyrexTypes.c_py_ssize_t_type, None),
            PyrexTypes.CFuncTypeArg("end", PyrexTypes.c_py_ssize_t_type, None),
            ],
        exception_value = '-1')

    def _handle_simple_method_unicode_count(self, node, args, is_unbound_method):
        """Replace unicode.count(...) by a direct call to the
        corresponding C-API function.
        """
        if len(args) not in (2,3,4):
            self._error_wrong_arg_count('unicode.count', node, args, "2-4")
            return node
        self._inject_int_default_argument(
            node, args, 2, PyrexTypes.c_py_ssize_t_type, "0")
        self._inject_int_default_argument(
            node, args, 3, PyrexTypes.c_py_ssize_t_type, "PY_SSIZE_T_MAX")

        method_call = self._substitute_method_call(
            node, "PyUnicode_Count", self.PyUnicode_Count_func_type,
            'count', is_unbound_method, args)
        return method_call.coerce_to_pyobject(self.current_env())

    PyUnicode_Replace_func_type = PyrexTypes.CFuncType(
        Builtin.unicode_type, [
            PyrexTypes.CFuncTypeArg("str", Builtin.unicode_type, None),
            PyrexTypes.CFuncTypeArg("substring", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("replstr", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("maxcount", PyrexTypes.c_py_ssize_t_type, None),
            ])

    def _handle_simple_method_unicode_replace(self, node, args, is_unbound_method):
        """Replace unicode.replace(...) by a direct call to the
        corresponding C-API function.
        """
        if len(args) not in (3,4):
            self._error_wrong_arg_count('unicode.replace', node, args, "3-4")
            return node
        self._inject_int_default_argument(
            node, args, 3, PyrexTypes.c_py_ssize_t_type, "-1")

        return self._substitute_method_call(
            node, "PyUnicode_Replace", self.PyUnicode_Replace_func_type,
            'replace', is_unbound_method, args)

    PyUnicode_AsEncodedString_func_type = PyrexTypes.CFuncType(
        Builtin.bytes_type, [
            PyrexTypes.CFuncTypeArg("obj", Builtin.unicode_type, None),
            PyrexTypes.CFuncTypeArg("encoding", PyrexTypes.c_char_ptr_type, None),
            PyrexTypes.CFuncTypeArg("errors", PyrexTypes.c_char_ptr_type, None),
            ])

    PyUnicode_AsXyzString_func_type = PyrexTypes.CFuncType(
        Builtin.bytes_type, [
            PyrexTypes.CFuncTypeArg("obj", Builtin.unicode_type, None),
            ])

    _special_encodings = ['UTF8', 'UTF16', 'Latin1', 'ASCII',
                          'unicode_escape', 'raw_unicode_escape']

    _special_codecs = [ (name, codecs.getencoder(name))
                        for name in _special_encodings ]

    def _handle_simple_method_unicode_encode(self, node, args, is_unbound_method):
        """Replace unicode.encode(...) by a direct C-API call to the
        corresponding codec.
        """
        if len(args) < 1 or len(args) > 3:
            self._error_wrong_arg_count('unicode.encode', node, args, '1-3')
            return node

        string_node = args[0]

        if len(args) == 1:
            null_node = ExprNodes.NullNode(node.pos)
            return self._substitute_method_call(
                node, "PyUnicode_AsEncodedString",
                self.PyUnicode_AsEncodedString_func_type,
                'encode', is_unbound_method, [string_node, null_node, null_node])

        parameters = self._unpack_encoding_and_error_mode(node.pos, args)
        if parameters is None:
            return node
        encoding, encoding_node, error_handling, error_handling_node = parameters

        if isinstance(string_node, ExprNodes.UnicodeNode):
            # constant, so try to do the encoding at compile time
            try:
                value = string_node.value.encode(encoding, error_handling)
            except:
                # well, looks like we can't
                pass
            else:
                value = BytesLiteral(value)
                value.encoding = encoding
                return ExprNodes.BytesNode(
                    string_node.pos, value=value, type=Builtin.bytes_type)

        if error_handling == 'strict':
            # try to find a specific encoder function
            codec_name = self._find_special_codec_name(encoding)
            if codec_name is not None:
                encode_function = "PyUnicode_As%sString" % codec_name
                return self._substitute_method_call(
                    node, encode_function,
                    self.PyUnicode_AsXyzString_func_type,
                    'encode', is_unbound_method, [string_node])

        return self._substitute_method_call(
            node, "PyUnicode_AsEncodedString",
            self.PyUnicode_AsEncodedString_func_type,
            'encode', is_unbound_method,
            [string_node, encoding_node, error_handling_node])

    PyUnicode_DecodeXyz_func_type = PyrexTypes.CFuncType(
        Builtin.unicode_type, [
            PyrexTypes.CFuncTypeArg("string", PyrexTypes.c_char_ptr_type, None),
            PyrexTypes.CFuncTypeArg("size", PyrexTypes.c_py_ssize_t_type, None),
            PyrexTypes.CFuncTypeArg("errors", PyrexTypes.c_char_ptr_type, None),
            ])

    PyUnicode_Decode_func_type = PyrexTypes.CFuncType(
        Builtin.unicode_type, [
            PyrexTypes.CFuncTypeArg("string", PyrexTypes.c_char_ptr_type, None),
            PyrexTypes.CFuncTypeArg("size", PyrexTypes.c_py_ssize_t_type, None),
            PyrexTypes.CFuncTypeArg("encoding", PyrexTypes.c_char_ptr_type, None),
            PyrexTypes.CFuncTypeArg("errors", PyrexTypes.c_char_ptr_type, None),
            ])

    def _handle_simple_method_bytes_decode(self, node, args, is_unbound_method):
        """Replace char*.decode() by a direct C-API call to the
        corresponding codec, possibly resoving a slice on the char*.
        """
        if len(args) < 1 or len(args) > 3:
            self._error_wrong_arg_count('bytes.decode', node, args, '1-3')
            return node
        temps = []
        if isinstance(args[0], ExprNodes.SliceIndexNode):
            index_node = args[0]
            string_node = index_node.base
            if not string_node.type.is_string:
                # nothing to optimise here
                return node
            start, stop = index_node.start, index_node.stop
            if not start or start.constant_result == 0:
                start = None
            else:
                if start.type.is_pyobject:
                    start = start.coerce_to(PyrexTypes.c_py_ssize_t_type, self.current_env())
                if stop:
                    start = UtilNodes.LetRefNode(start)
                    temps.append(start)
                string_node = ExprNodes.AddNode(pos=start.pos,
                                                operand1=string_node,
                                                operator='+',
                                                operand2=start,
                                                is_temp=False,
                                                type=string_node.type
                                                )
            if stop and stop.type.is_pyobject:
                stop = stop.coerce_to(PyrexTypes.c_py_ssize_t_type, self.current_env())
        elif isinstance(args[0], ExprNodes.CoerceToPyTypeNode) \
                 and args[0].arg.type.is_string:
            # use strlen() to find the string length, just as CPython would
            start = stop = None
            string_node = args[0].arg
        else:
            # let Python do its job
            return node

        if not stop:
            if start or not string_node.is_name:
                string_node = UtilNodes.LetRefNode(string_node)
                temps.append(string_node)
            stop = ExprNodes.PythonCapiCallNode(
                string_node.pos, "strlen", self.Pyx_strlen_func_type,
                    args = [string_node],
                    is_temp = False,
                    utility_code = UtilityCode.load_cached("IncludeStringH", "StringTools.c"),
                    ).coerce_to(PyrexTypes.c_py_ssize_t_type, self.current_env())
        elif start:
            stop = ExprNodes.SubNode(
                pos = stop.pos,
                operand1 = stop,
                operator = '-',
                operand2 = start,
                is_temp = False,
                type = PyrexTypes.c_py_ssize_t_type
                )

        parameters = self._unpack_encoding_and_error_mode(node.pos, args)
        if parameters is None:
            return node
        encoding, encoding_node, error_handling, error_handling_node = parameters

        # try to find a specific encoder function
        codec_name = None
        if encoding is not None:
            codec_name = self._find_special_codec_name(encoding)
        if codec_name is not None:
            decode_function = "PyUnicode_Decode%s" % codec_name
            node = ExprNodes.PythonCapiCallNode(
                node.pos, decode_function,
                self.PyUnicode_DecodeXyz_func_type,
                args = [string_node, stop, error_handling_node],
                is_temp = node.is_temp,
                )
        else:
            node = ExprNodes.PythonCapiCallNode(
                node.pos, "PyUnicode_Decode",
                self.PyUnicode_Decode_func_type,
                args = [string_node, stop, encoding_node, error_handling_node],
                is_temp = node.is_temp,
                )

        for temp in temps[::-1]:
            node = UtilNodes.EvalWithTempExprNode(temp, node)
        return node

    def _find_special_codec_name(self, encoding):
        try:
            requested_codec = codecs.getencoder(encoding)
        except:
            return None
        for name, codec in self._special_codecs:
            if codec == requested_codec:
                if '_' in name:
                    name = ''.join([ s.capitalize()
                                     for s in name.split('_')])
                return name
        return None

    def _unpack_encoding_and_error_mode(self, pos, args):
        null_node = ExprNodes.NullNode(pos)

        if len(args) >= 2:
            encoding_node = args[1]
            if isinstance(encoding_node, ExprNodes.CoerceToPyTypeNode):
                encoding_node = encoding_node.arg
            if isinstance(encoding_node, (ExprNodes.UnicodeNode, ExprNodes.StringNode,
                                          ExprNodes.BytesNode)):
                encoding = encoding_node.value
                encoding_node = ExprNodes.BytesNode(encoding_node.pos, value=encoding,
                                                     type=PyrexTypes.c_char_ptr_type)
            elif encoding_node.type is Builtin.bytes_type:
                encoding = None
                encoding_node = encoding_node.coerce_to(
                    PyrexTypes.c_char_ptr_type, self.current_env())
            elif encoding_node.type.is_string:
                encoding = None
            else:
                return None
        else:
            encoding = None
            encoding_node = null_node

        if len(args) == 3:
            error_handling_node = args[2]
            if isinstance(error_handling_node, ExprNodes.CoerceToPyTypeNode):
                error_handling_node = error_handling_node.arg
            if isinstance(error_handling_node,
                          (ExprNodes.UnicodeNode, ExprNodes.StringNode,
                           ExprNodes.BytesNode)):
                error_handling = error_handling_node.value
                if error_handling == 'strict':
                    error_handling_node = null_node
                else:
                    error_handling_node = ExprNodes.BytesNode(
                        error_handling_node.pos, value=error_handling,
                        type=PyrexTypes.c_char_ptr_type)
            elif error_handling_node.type is Builtin.bytes_type:
                error_handling = None
                error_handling_node = error_handling_node.coerce_to(
                    PyrexTypes.c_char_ptr_type, self.current_env())
            elif error_handling_node.type.is_string:
                error_handling = None
            else:
                return None
        else:
            error_handling = 'strict'
            error_handling_node = null_node

        return (encoding, encoding_node, error_handling, error_handling_node)

    def _handle_simple_method_str_endswith(self, node, args, is_unbound_method):
        return self._inject_tailmatch(
            node, args, is_unbound_method, 'str', 'endswith',
            str_tailmatch_utility_code, +1)

    def _handle_simple_method_str_startswith(self, node, args, is_unbound_method):
        return self._inject_tailmatch(
            node, args, is_unbound_method, 'str', 'startswith',
            str_tailmatch_utility_code, -1)

    def _handle_simple_method_bytes_endswith(self, node, args, is_unbound_method):
        return self._inject_tailmatch(
            node, args, is_unbound_method, 'bytes', 'endswith',
            bytes_tailmatch_utility_code, +1)

    def _handle_simple_method_bytes_startswith(self, node, args, is_unbound_method):
        return self._inject_tailmatch(
            node, args, is_unbound_method, 'bytes', 'startswith',
            bytes_tailmatch_utility_code, -1)

    ### helpers

    def _substitute_method_call(self, node, name, func_type,
                                attr_name, is_unbound_method, args=(),
                                utility_code=None, is_temp=None,
                                may_return_none=ExprNodes.PythonCapiCallNode.may_return_none):
        args = list(args)
        if args and not args[0].is_literal:
            self_arg = args[0]
            if is_unbound_method:
                self_arg = self_arg.as_none_safe_node(
                    "descriptor '%s' requires a '%s' object but received a 'NoneType'",
                    format_args = [attr_name, node.function.obj.name])
            else:
                self_arg = self_arg.as_none_safe_node(
                    "'NoneType' object has no attribute '%s'",
                    error = "PyExc_AttributeError",
                    format_args = [attr_name])
            args[0] = self_arg
        if is_temp is None:
            is_temp = node.is_temp
        return ExprNodes.PythonCapiCallNode(
            node.pos, name, func_type,
            args = args,
            is_temp = is_temp,
            utility_code = utility_code,
            may_return_none = may_return_none,
            result_is_used = node.result_is_used,
            )

    def _inject_int_default_argument(self, node, args, arg_index, type, default_value):
        assert len(args) >= arg_index
        if len(args) == arg_index:
            args.append(ExprNodes.IntNode(node.pos, value=str(default_value),
                                          type=type, constant_result=default_value))
        else:
            args[arg_index] = args[arg_index].coerce_to(type, self.current_env())

    def _inject_bint_default_argument(self, node, args, arg_index, default_value):
        assert len(args) >= arg_index
        if len(args) == arg_index:
            default_value = bool(default_value)
            args.append(ExprNodes.BoolNode(node.pos, value=default_value,
                                           constant_result=default_value))
        else:
            args[arg_index] = args[arg_index].coerce_to_boolean(self.current_env())


unicode_tailmatch_utility_code = load_c_utility('unicode_tailmatch')

bytes_tailmatch_utility_code = load_c_utility('bytes_tailmatch')

str_tailmatch_utility_code = UtilityCode(
proto = '''
static CYTHON_INLINE int __Pyx_PyStr_Tailmatch(PyObject* self, PyObject* arg, Py_ssize_t start,
                                               Py_ssize_t end, int direction);
''',
# We do not use a C compiler macro here to avoid "unused function"
# warnings for the *_Tailmatch() function that is not being used in
# the specific CPython version.  The C compiler will generate the same
# code anyway, and will usually just remove the unused function.
impl = '''
static CYTHON_INLINE int __Pyx_PyStr_Tailmatch(PyObject* self, PyObject* arg, Py_ssize_t start,
                                               Py_ssize_t end, int direction)
{
    if (PY_MAJOR_VERSION < 3)
        return __Pyx_PyBytes_Tailmatch(self, arg, start, end, direction);
    else
        return __Pyx_PyUnicode_Tailmatch(self, arg, start, end, direction);
}
''',
requires=[unicode_tailmatch_utility_code, bytes_tailmatch_utility_code]
)


tpnew_utility_code = UtilityCode(
proto = """
static CYTHON_INLINE PyObject* __Pyx_tp_new(PyObject* type_obj) {
    return (PyObject*) (((PyTypeObject*)(type_obj))->tp_new(
        (PyTypeObject*)(type_obj), %(TUPLE)s, NULL));
}
""" % {'TUPLE' : Naming.empty_tuple}
)


class ConstantFolding(Visitor.VisitorTransform, SkipDeclarations):
    """Calculate the result of constant expressions to store it in
    ``expr_node.constant_result``, and replace trivial cases by their
    constant result.

    General rules:

    - We calculate float constants to make them available to the
      compiler, but we do not aggregate them into a single literal
      node to prevent any loss of precision.

    - We recursively calculate constants from non-literal nodes to
      make them available to the compiler, but we only aggregate
      literal nodes at each step.  Non-literal nodes are never merged
      into a single node.
    """

    def __init__(self, reevaluate=False):
        """
        The reevaluate argument specifies whether constant values that were
        previously computed should be recomputed.
        """
        super(ConstantFolding, self).__init__()
        self.reevaluate = reevaluate

    def _calculate_const(self, node):
        if (not self.reevaluate and
                node.constant_result is not ExprNodes.constant_value_not_set):
            return

        # make sure we always set the value
        not_a_constant = ExprNodes.not_a_constant
        node.constant_result = not_a_constant

        # check if all children are constant
        children = self.visitchildren(node)
        for child_result in children.values():
            if type(child_result) is list:
                for child in child_result:
                    if getattr(child, 'constant_result', not_a_constant) is not_a_constant:
                        return
            elif getattr(child_result, 'constant_result', not_a_constant) is not_a_constant:
                return

        # now try to calculate the real constant value
        try:
            node.calculate_constant_result()
#            if node.constant_result is not ExprNodes.not_a_constant:
#                print node.__class__.__name__, node.constant_result
        except (ValueError, TypeError, KeyError, IndexError, AttributeError, ArithmeticError):
            # ignore all 'normal' errors here => no constant result
            pass
        except Exception:
            # this looks like a real error
            import traceback, sys
            traceback.print_exc(file=sys.stdout)

    NODE_TYPE_ORDER = [ExprNodes.CharNode, ExprNodes.IntNode,
                       ExprNodes.LongNode, ExprNodes.FloatNode]

    def _widest_node_class(self, *nodes):
        try:
            return self.NODE_TYPE_ORDER[
                max(map(self.NODE_TYPE_ORDER.index, map(type, nodes)))]
        except ValueError:
            return None

    def visit_ExprNode(self, node):
        self._calculate_const(node)
        return node

    def visit_UnopNode(self, node):
        self._calculate_const(node)
        if node.constant_result is ExprNodes.not_a_constant:
            return node
        if not node.operand.is_literal:
            return node
        if isinstance(node.operand, ExprNodes.BoolNode):
            return ExprNodes.IntNode(node.pos, value = str(node.constant_result),
                                     type = PyrexTypes.c_int_type,
                                     constant_result = node.constant_result)
        if node.operator == '+':
            return self._handle_UnaryPlusNode(node)
        elif node.operator == '-':
            return self._handle_UnaryMinusNode(node)
        return node

    def _handle_UnaryMinusNode(self, node):
        if isinstance(node.operand, ExprNodes.LongNode):
            return ExprNodes.LongNode(node.pos, value = '-' + node.operand.value,
                                      constant_result = node.constant_result)
        if isinstance(node.operand, ExprNodes.FloatNode):
            # this is a safe operation
            return ExprNodes.FloatNode(node.pos, value = '-' + node.operand.value,
                                       constant_result = node.constant_result)
        node_type = node.operand.type
        if node_type.is_int and node_type.signed or \
               isinstance(node.operand, ExprNodes.IntNode) and node_type.is_pyobject:
            return ExprNodes.IntNode(node.pos, value = '-' + node.operand.value,
                                     type = node_type,
                                     longness = node.operand.longness,
                                     constant_result = node.constant_result)
        return node

    def _handle_UnaryPlusNode(self, node):
        if node.constant_result == node.operand.constant_result:
            return node.operand
        return node

    def visit_BoolBinopNode(self, node):
        self._calculate_const(node)
        if node.constant_result is ExprNodes.not_a_constant:
            return node
        if not node.operand1.is_literal or not node.operand2.is_literal:
            return node

        if node.constant_result == node.operand1.constant_result and node.operand1.is_literal:
            return node.operand1
        elif node.constant_result == node.operand2.constant_result and node.operand2.is_literal:
            return node.operand2
        else:
            # FIXME: we could do more ...
            return node

    def visit_BinopNode(self, node):
        self._calculate_const(node)
        if node.constant_result is ExprNodes.not_a_constant:
            return node
        if isinstance(node.constant_result, float):
            return node
        operand1, operand2 = node.operand1, node.operand2
        if not operand1.is_literal or not operand2.is_literal:
            return node

        # now inject a new constant node with the calculated value
        try:
            type1, type2 = operand1.type, operand2.type
            if type1 is None or type2 is None:
                return node
        except AttributeError:
            return node

        if type1.is_numeric and type2.is_numeric:
            widest_type = PyrexTypes.widest_numeric_type(type1, type2)
        else:
            widest_type = PyrexTypes.py_object_type
        target_class = self._widest_node_class(operand1, operand2)
        if target_class is None:
            return node
        elif target_class is ExprNodes.IntNode:
            unsigned = getattr(operand1, 'unsigned', '') and \
                       getattr(operand2, 'unsigned', '')
            longness = "LL"[:max(len(getattr(operand1, 'longness', '')),
                                 len(getattr(operand2, 'longness', '')))]
            new_node = ExprNodes.IntNode(pos=node.pos,
                                         unsigned = unsigned, longness = longness,
                                         value = str(node.constant_result),
                                         constant_result = node.constant_result)
            # IntNode is smart about the type it chooses, so we just
            # make sure we were not smarter this time
            if widest_type.is_pyobject or new_node.type.is_pyobject:
                new_node.type = PyrexTypes.py_object_type
            else:
                new_node.type = PyrexTypes.widest_numeric_type(widest_type, new_node.type)
        else:
            if isinstance(node, ExprNodes.BoolNode):
                node_value = node.constant_result
            else:
                node_value = str(node.constant_result)
            new_node = target_class(pos=node.pos, type = widest_type,
                                    value = node_value,
                                    constant_result = node.constant_result)
        return new_node

    def visit_MulNode(self, node):
        if isinstance(node.operand1, (ExprNodes.ListNode, ExprNodes.TupleNode)):
            sequence_node = node.operand1
            factor = node.operand2
            self._calculate_const(factor)
            if factor.constant_result != 1:
                sequence_node.mult_factor = factor
            self.visitchildren(sequence_node)
            return sequence_node
        if isinstance(node.operand1, ExprNodes.IntNode) and \
               isinstance(node.operand2, (ExprNodes.ListNode, ExprNodes.TupleNode)):
            sequence_node = node.operand2
            factor = node.operand1
            self._calculate_const(factor)
            if factor.constant_result != 1:
                sequence_node.mult_factor = factor
            self.visitchildren(sequence_node)
            return sequence_node
        return self.visit_BinopNode(node)

    def visit_PrimaryCmpNode(self, node):
        self._calculate_const(node)
        if node.constant_result is ExprNodes.not_a_constant:
            return node
        bool_result = bool(node.constant_result)
        return ExprNodes.BoolNode(node.pos, value=bool_result,
                                  constant_result=bool_result)

    def visit_CondExprNode(self, node):
        self._calculate_const(node)
        if node.test.constant_result is ExprNodes.not_a_constant:
            return node
        if node.test.constant_result:
            return node.true_val
        else:
            return node.false_val

    def visit_IfStatNode(self, node):
        self.visitchildren(node)
        # eliminate dead code based on constant condition results
        if_clauses = []
        for if_clause in node.if_clauses:
            condition_result = if_clause.get_constant_condition_result()
            if condition_result is None:
                # unknown result => normal runtime evaluation
                if_clauses.append(if_clause)
            elif condition_result == True:
                # subsequent clauses can safely be dropped
                node.else_clause = if_clause.body
                break
            else:
                assert condition_result == False
        if not if_clauses:
            return node.else_clause
        node.if_clauses = if_clauses
        return node

    # in the future, other nodes can have their own handler method here
    # that can replace them with a constant result node

    visit_Node = Visitor.VisitorTransform.recurse_to_children


class FinalOptimizePhase(Visitor.CythonTransform):
    """
    This visitor handles several commuting optimizations, and is run
    just before the C code generation phase.

    The optimizations currently implemented in this class are:
        - eliminate None assignment and refcounting for first assignment.
        - isinstance -> typecheck for cdef types
        - eliminate checks for None and/or types that became redundant after tree changes
    """
    def visit_SingleAssignmentNode(self, node):
        """Avoid redundant initialisation of local variables before their
        first assignment.
        """
        self.visitchildren(node)
        if node.first:
            lhs = node.lhs
            lhs.lhs_of_first_assignment = True
        return node

    def visit_SimpleCallNode(self, node):
        """Replace generic calls to isinstance(x, type) by a more efficient
        type check.
        """
        self.visitchildren(node)
        if node.function.type.is_cfunction and isinstance(node.function, ExprNodes.NameNode):
            if node.function.name == 'isinstance':
                type_arg = node.args[1]
                if type_arg.type.is_builtin_type and type_arg.type.name == 'type':
                    cython_scope = self.context.cython_scope
                    node.function.entry = cython_scope.lookup('PyObject_TypeCheck')
                    node.function.type = node.function.entry.type
                    PyTypeObjectPtr = PyrexTypes.CPtrType(cython_scope.lookup('PyTypeObject').type)
                    node.args[1] = ExprNodes.CastNode(node.args[1], PyTypeObjectPtr)
        return node

    def visit_PyTypeTestNode(self, node):
        """Remove tests for alternatively allowed None values from
        type tests when we know that the argument cannot be None
        anyway.
        """
        self.visitchildren(node)
        if not node.notnone:
            if not node.arg.may_be_none():
                node.notnone = True
        return node

    def visit_NoneCheckNode(self, node):
        """Remove None checks from expressions that definitely do not
        carry a None value.
        """
        self.visitchildren(node)
        if not node.arg.may_be_none():
            return node.arg
        return node
