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
    reduce
except NameError:
    from functools import reduce

try:
    set
except NameError:
    from sets import Set as set

class FakePythonEnv(object):
    "A fake environment for creating type test nodes etc."
    nogil = False

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
    PyDict_Next_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_bint_type, [
            PyrexTypes.CFuncTypeArg("dict",  PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("pos",   PyrexTypes.c_py_ssize_t_ptr_type, None),
            PyrexTypes.CFuncTypeArg("key",   PyrexTypes.CPtrType(PyrexTypes.py_object_type), None),
            PyrexTypes.CFuncTypeArg("value", PyrexTypes.CPtrType(PyrexTypes.py_object_type), None)
            ])

    PyDict_Next_name = EncodedString("PyDict_Next")

    PyDict_Next_entry = Symtab.Entry(
        PyDict_Next_name, PyDict_Next_name, PyDict_Next_func_type)

    visit_Node = Visitor.VisitorTransform.recurse_to_children

    def visit_ModuleNode(self, node):
        self.current_scope = node.scope
        self.visitchildren(node)
        return node

    def visit_DefNode(self, node):
        oldscope = self.current_scope
        self.current_scope = node.entry.scope
        self.visitchildren(node)
        self.current_scope = oldscope
        return node

    def visit_ForInStatNode(self, node):
        self.visitchildren(node)
        return self._optimise_for_loop(node)

    def _optimise_for_loop(self, node):
        iterator = node.iterator.sequence
        if iterator.type is Builtin.dict_type:
            # like iterating over dict.keys()
            return self._transform_dict_iteration(
                node, dict_obj=iterator, keys=True, values=False)

        # C array slice iteration?
        if isinstance(iterator, ExprNodes.SliceIndexNode) and \
               (iterator.base.type.is_array or iterator.base.type.is_ptr):
            return self._transform_carray_iteration(node, iterator)
        elif not isinstance(iterator, ExprNodes.SimpleCallNode):
            return node

        function = iterator.function
        # dict iteration?
        if isinstance(function, ExprNodes.AttributeNode) and \
                function.obj.type == Builtin.dict_type:
            dict_obj = function.obj
            method = function.attribute

            keys = values = False
            if method == 'iterkeys':
                keys = True
            elif method == 'itervalues':
                values = True
            elif method == 'iteritems':
                keys = values = True
            else:
                return node
            return self._transform_dict_iteration(
                node, dict_obj, keys, values)

        # enumerate() ?
        if iterator.self is None and function.is_name and \
               function.entry and function.entry.is_builtin and \
               function.name == 'enumerate':
            return self._transform_enumerate_iteration(node, iterator)

        # range() iteration?
        if Options.convert_range and node.target.type.is_int:
            if iterator.self is None and function.is_name and \
                   function.entry and function.entry.is_builtin and \
                   function.name in ('range', 'xrange'):
                return self._transform_range_iteration(node, iterator)

        return node

    def _transform_carray_iteration(self, node, slice_node):
        start = slice_node.start
        stop = slice_node.stop
        step = None
        if not stop:
            return node

        carray_ptr = slice_node.base.coerce_to_simple(self.current_scope)

        if start and start.constant_result != 0:
            start_ptr_node = ExprNodes.AddNode(
                start.pos,
                operand1=carray_ptr,
                operator='+',
                operand2=start,
                type=carray_ptr.type)
        else:
            start_ptr_node = carray_ptr

        stop_ptr_node = ExprNodes.AddNode(
            stop.pos,
            operand1=carray_ptr,
            operator='+',
            operand2=stop,
            type=carray_ptr.type
            ).coerce_to_simple(self.current_scope)

        counter = UtilNodes.TempHandle(carray_ptr.type)
        counter_temp = counter.ref(node.target.pos)

        if slice_node.base.type.is_string and node.target.type.is_pyobject:
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
        else:
            target_value = ExprNodes.IndexNode(
                node.target.pos,
                index=ExprNodes.IntNode(node.target.pos, value='0',
                                        constant_result=0,
                                        type=PyrexTypes.c_int_type),
                base=counter_temp,
                is_buffer_access=False,
                type=carray_ptr.type.base_type)

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

        for_node = Nodes.ForFromStatNode(
            node.pos,
            bound1=start_ptr_node, relation1='<=',
            target=counter_temp,
            relation2='<', bound2=stop_ptr_node,
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
        return UtilNodes.LetNode(temp, self._optimise_for_loop(node))

    def _transform_range_iteration(self, node, range_function):
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
            if not isinstance(step, ExprNodes.IntNode):
                step = ExprNodes.IntNode(step_pos, value=str(step_value),
                                         constant_result=step_value)

        if step_value < 0:
            step.value = str(-step_value)
            relation1 = '>='
            relation2 = '>'
        else:
            relation1 = '<='
            relation2 = '<'

        if len(args) == 1:
            bound1 = ExprNodes.IntNode(range_function.pos, value='0',
                                       constant_result=0)
            bound2 = args[0].coerce_to_integer(self.current_scope)
        else:
            bound1 = args[0].coerce_to_integer(self.current_scope)
            bound2 = args[1].coerce_to_integer(self.current_scope)
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

    def _transform_dict_iteration(self, node, dict_obj, keys, values):
        py_object_ptr = PyrexTypes.c_void_ptr_type

        temps = []
        temp = UtilNodes.TempHandle(PyrexTypes.py_object_type)
        temps.append(temp)
        dict_temp = temp.ref(dict_obj.pos)
        temp = UtilNodes.TempHandle(PyrexTypes.c_py_ssize_t_type)
        temps.append(temp)
        pos_temp = temp.ref(node.pos)
        pos_temp_addr = ExprNodes.AmpersandNode(
            node.pos, operand=pos_temp,
            type=PyrexTypes.c_ptr_type(PyrexTypes.c_py_ssize_t_type))
        if keys:
            temp = UtilNodes.TempHandle(py_object_ptr)
            temps.append(temp)
            key_temp = temp.ref(node.target.pos)
            key_temp_addr = ExprNodes.AmpersandNode(
                node.target.pos, operand=key_temp,
                type=PyrexTypes.c_ptr_type(py_object_ptr))
        else:
            key_temp_addr = key_temp = ExprNodes.NullNode(
                pos=node.target.pos)
        if values:
            temp = UtilNodes.TempHandle(py_object_ptr)
            temps.append(temp)
            value_temp = temp.ref(node.target.pos)
            value_temp_addr = ExprNodes.AmpersandNode(
                node.target.pos, operand=value_temp,
                type=PyrexTypes.c_ptr_type(py_object_ptr))
        else:
            value_temp_addr = value_temp = ExprNodes.NullNode(
                pos=node.target.pos)

        key_target = value_target = node.target
        tuple_target = None
        if keys and values:
            if node.target.is_sequence_constructor:
                if len(node.target.args) == 2:
                    key_target, value_target = node.target.args
                else:
                    # unusual case that may or may not lead to an error
                    return node
            else:
                tuple_target = node.target

        def coerce_object_to(obj_node, dest_type):
            if dest_type.is_pyobject:
                if dest_type != obj_node.type:
                    if dest_type.is_extension_type or dest_type.is_builtin_type:
                        obj_node = ExprNodes.PyTypeTestNode(
                            obj_node, dest_type, self.current_scope, notnone=True)
                result = ExprNodes.TypecastNode(
                    obj_node.pos,
                    operand = obj_node,
                    type = dest_type)
                return (result, None)
            else:
                temp = UtilNodes.TempHandle(dest_type)
                temps.append(temp)
                temp_result = temp.ref(obj_node.pos)
                class CoercedTempNode(ExprNodes.CoerceFromPyTypeNode):
                    def result(self):
                        return temp_result.result()
                    def generate_execution_code(self, code):
                        self.generate_result_code(code)
                return (temp_result, CoercedTempNode(dest_type, obj_node, self.current_scope))

        if isinstance(node.body, Nodes.StatListNode):
            body = node.body
        else:
            body = Nodes.StatListNode(pos = node.body.pos,
                                      stats = [node.body])

        if tuple_target:
            tuple_result = ExprNodes.TupleNode(
                pos = tuple_target.pos,
                args = [key_temp, value_temp],
                is_temp = 1,
                type = Builtin.tuple_type,
                )
            body.stats.insert(
                0, Nodes.SingleAssignmentNode(
                    pos = tuple_target.pos,
                    lhs = tuple_target,
                    rhs = tuple_result))
        else:
            # execute all coercions before the assignments
            coercion_stats = []
            assign_stats = []
            if keys:
                temp_result, coercion = coerce_object_to(
                    key_temp, key_target.type)
                if coercion:
                    coercion_stats.append(coercion)
                assign_stats.append(
                    Nodes.SingleAssignmentNode(
                        pos = key_temp.pos,
                        lhs = key_target,
                        rhs = temp_result))
            if values:
                temp_result, coercion = coerce_object_to(
                    value_temp, value_target.type)
                if coercion:
                    coercion_stats.append(coercion)
                assign_stats.append(
                    Nodes.SingleAssignmentNode(
                        pos = value_temp.pos,
                        lhs = value_target,
                        rhs = temp_result))
            body.stats[0:0] = coercion_stats + assign_stats

        result_code = [
            Nodes.SingleAssignmentNode(
                pos = dict_obj.pos,
                lhs = dict_temp,
                rhs = dict_obj),
            Nodes.SingleAssignmentNode(
                pos = node.pos,
                lhs = pos_temp,
                rhs = ExprNodes.IntNode(node.pos, value='0',
                                        constant_result=0)),
            Nodes.WhileStatNode(
                pos = node.pos,
                condition = ExprNodes.SimpleCallNode(
                    pos = dict_obj.pos,
                    type = PyrexTypes.c_bint_type,
                    function = ExprNodes.NameNode(
                        pos = dict_obj.pos,
                        name = self.PyDict_Next_name,
                        type = self.PyDict_Next_func_type,
                        entry = self.PyDict_Next_entry),
                    args = [dict_temp, pos_temp_addr,
                            key_temp_addr, value_temp_addr]
                    ),
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


class SwitchTransform(Visitor.VisitorTransform):
    """
    This transformation tries to turn long if statements into C switch statements. 
    The requirement is that every clause be an (or of) var == value, where the var
    is common among all clauses and both var and value are ints. 
    """
    def extract_conditions(self, cond):
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

        if (isinstance(cond, ExprNodes.PrimaryCmpNode) 
                and cond.cascade is None 
                and cond.operator == '=='
                and not cond.is_python_comparison()):
            if is_common_value(cond.operand1, cond.operand1):
                if cond.operand2.is_literal:
                    return cond.operand1, [cond.operand2]
                elif hasattr(cond.operand2, 'entry') and cond.operand2.entry and cond.operand2.entry.is_const:
                    return cond.operand1, [cond.operand2]
            if is_common_value(cond.operand2, cond.operand2):
                if cond.operand1.is_literal:
                    return cond.operand2, [cond.operand1]
                elif hasattr(cond.operand1, 'entry') and cond.operand1.entry and cond.operand1.entry.is_const:
                    return cond.operand2, [cond.operand1]
        elif (isinstance(cond, ExprNodes.BoolBinopNode) 
                and cond.operator == 'or'):
            t1, c1 = self.extract_conditions(cond.operand1)
            t2, c2 = self.extract_conditions(cond.operand2)
            if is_common_value(t1, t2):
                return t1, c1+c2
        return None, None
        
    def visit_IfStatNode(self, node):
        self.visitchildren(node)
        common_var = None
        case_count = 0
        cases = []
        for if_clause in node.if_clauses:
            var, conditions = self.extract_conditions(if_clause.condition)
            if var is None:
                return node
            elif common_var is not None and not is_common_value(var, common_var):
                return node
            elif not var.type.is_int or sum([not cond.type.is_int for cond in conditions]):
                return node
            else:
                common_var = var
                case_count += len(conditions)
                cases.append(Nodes.SwitchCaseNode(pos = if_clause.pos,
                                                  conditions = conditions,
                                                  body = if_clause.body))
        if case_count < 2:
            return node
        
        common_var = unwrap_node(common_var)
        return Nodes.SwitchStatNode(pos = node.pos,
                                    test = common_var,
                                    cases = cases,
                                    else_clause = node.else_clause)

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

        if not isinstance(node.operand2, (ExprNodes.TupleNode, ExprNodes.ListNode)):
            return node

        args = node.operand2.args
        if len(args) == 0:
            return ExprNodes.BoolNode(pos = node.pos, value = node.operator == 'not_in')

        lhs = UtilNodes.ResultRefNode(node.operand1)

        conds = []
        for arg in args:
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
        return UtilNodes.EvalWithTempExprNode(lhs, condition)

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
        entry = self.env_stack[-1].lookup(function.name)
        if not entry or getattr(entry, 'scope', None) is not Builtin.builtin_scope:
            return False
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

    def _handle_simple_function_set(self, node, pos_args):
        """Replace set([a,b,...]) by a literal set {a,b,...} and
        set([ x for ... ]) by a literal { x for ... }.
        """
        arg_count = len(pos_args)
        if arg_count == 0:
            return ExprNodes.SetNode(node.pos, args=[],
                                     type=Builtin.set_type)
        if arg_count > 1:
            return node
        iterable = pos_args[0]
        if isinstance(iterable, (ExprNodes.ListNode, ExprNodes.TupleNode)):
            return ExprNodes.SetNode(node.pos, args=iterable.args)
        elif isinstance(iterable, ExprNodes.ComprehensionNode) and \
                 isinstance(iterable.target, (ExprNodes.ListNode,
                                              ExprNodes.SetNode)):
            iterable.target = ExprNodes.SetNode(node.pos, args=[])
            iterable.pos = node.pos
            return iterable
        else:
            return node

    def _handle_simple_function_dict(self, node, pos_args):
        """Replace dict([ (a,b) for ... ]) by a literal { a:b for ... }.
        """
        if len(pos_args) != 1:
            return node
        arg = pos_args[0]
        if isinstance(arg, ExprNodes.ComprehensionNode) and \
               isinstance(arg.target, (ExprNodes.ListNode,
                                       ExprNodes.SetNode)):
            append_node = arg.append
            if isinstance(append_node.expr, (ExprNodes.TupleNode, ExprNodes.ListNode)) and \
                   len(append_node.expr.args) == 2:
                key_node, value_node = append_node.expr.args
                target_node = ExprNodes.DictNode(
                    pos=arg.target.pos, key_value_pairs=[])
                new_append_node = ExprNodes.DictComprehensionAppendNode(
                    append_node.pos, target=target_node,
                    key_expr=key_node, value_expr=value_node)
                arg.target = target_node
                arg.type = target_node.type
                replace_in = Visitor.RecursiveNodeReplacer(append_node, new_append_node)
                return replace_in(arg)
        return node

    def _handle_simple_function_float(self, node, pos_args):
        if len(pos_args) == 0:
            return ExprNodes.FloatNode(node.pos, value='0.0')
        if len(pos_args) > 1:
            self._error_wrong_arg_count('float', node, pos_args, 1)
        return node

    # specific handlers for general call nodes

    def _handle_general_function_dict(self, node, pos_args, kwargs):
        """Replace dict(a=b,c=d,...) by the underlying keyword dict
        construction which is done anyway.
        """
        if len(pos_args) > 0:
            return node
        if not isinstance(kwargs, ExprNodes.DictNode):
            return node
        if node.starstar_arg:
            # we could optimize this by updating the kw dict instead
            return node
        return kwargs


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
        args = arg_tuple.args
        return self._dispatch_to_handler(
            node, function, args, node.keyword_args)

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
                return arg.coerce_to(node.type, self.env_stack[-1])
        if not isinstance(arg, ExprNodes.SimpleCallNode):
            return node
        if not (node.type.is_int or node.type.is_float):
            return node
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
            is_builtin = function.entry.is_builtin \
                         or getattr(function.entry, 'scope', None) is Builtin.builtin_scope
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
            arg = ExprNodes.NoneCheckNode(
                arg, "PyExc_TypeError", "'NoneType' is not iterable")
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
            pos_args[0] = ExprNodes.NoneCheckNode(
                list_arg, "PyExc_TypeError",
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

    def _handle_simple_function_float(self, node, pos_args):
        # Note: this requires the float() function to be typed as
        # returning a C 'double'
        if len(pos_args) != 1:
            self._error_wrong_arg_count('float', node, pos_args, 1)
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
            utility_code = pyobject_as_double_utility_code,
            py_name = "float")

    ### builtin functions

    PyObject_GetAttr2_func_type = PyrexTypes.CFuncType(
        PyrexTypes.py_object_type, [
            PyrexTypes.CFuncTypeArg("object", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("attr_name", PyrexTypes.py_object_type, None),
            ])

    PyObject_GetAttr3_func_type = PyrexTypes.CFuncType(
        PyrexTypes.py_object_type, [
            PyrexTypes.CFuncTypeArg("object", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("attr_name", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("default", PyrexTypes.py_object_type, None),
            ])

    def _handle_simple_function_getattr(self, node, pos_args):
        if len(pos_args) == 2:
            return ExprNodes.PythonCapiCallNode(
                node.pos, "PyObject_GetAttr", self.PyObject_GetAttr2_func_type,
                args = pos_args,
                is_temp = node.is_temp)
        elif len(pos_args) == 3:
            return ExprNodes.PythonCapiCallNode(
                node.pos, "__Pyx_GetAttr3", self.PyObject_GetAttr3_func_type,
                args = pos_args,
                is_temp = node.is_temp,
                utility_code = Builtin.getattr3_utility_code)
        else:
            self._error_wrong_arg_count('getattr', node, pos_args, '2 or 3')
        return node

    Pyx_strlen_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_size_t_type, [
            PyrexTypes.CFuncTypeArg("bytes", PyrexTypes.c_char_ptr_type, None)
            ])

    def _handle_simple_function_len(self, node, pos_args):
        # note: this only works because we already replaced len() by
        # PyObject_Length() which returns a Py_ssize_t instead of a
        # Python object, so we can return a plain size_t instead
        # without caring about Python object conversion etc.
        if len(pos_args) != 1:
            self._error_wrong_arg_count('len', node, pos_args, 1)
            return node
        arg = pos_args[0]
        if isinstance(arg, ExprNodes.CoerceToPyTypeNode):
            arg = arg.arg
        if not arg.type.is_string:
            return node
        node = ExprNodes.PythonCapiCallNode(
            node.pos, "strlen", self.Pyx_strlen_func_type,
            args = [arg],
            is_temp = node.is_temp,
            utility_code = include_string_h_utility_code
            )
        return node

    Pyx_Type_func_type = PyrexTypes.CFuncType(
        Builtin.type_type, [
            PyrexTypes.CFuncTypeArg("object", PyrexTypes.py_object_type, None)
            ])

    def _handle_simple_function_type(self, node, pos_args):
        if len(pos_args) != 1:
            return node
        node = ExprNodes.PythonCapiCallNode(
            node.pos, "Py_TYPE", self.Pyx_Type_func_type,
            args = pos_args,
            is_temp = False)
        return ExprNodes.CastNode(node, PyrexTypes.py_object_type)

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
            type_arg = ExprNodes.NoneCheckNode(
                type_arg, "PyExc_TypeError",
                "object.__new__(X): X is not a type object (NoneType)")

        return ExprNodes.PythonCapiCallNode(
            node.pos, "__Pyx_tp_new", self.Pyx_tp_new_func_type,
            args = [type_arg],
            utility_code = tpnew_utility_code,
            is_temp = node.is_temp
            )

    ### methods of builtin types

    PyObject_Append_func_type = PyrexTypes.CFuncType(
        PyrexTypes.py_object_type, [
            PyrexTypes.CFuncTypeArg("list", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("item", PyrexTypes.py_object_type, None),
            ])

    def _handle_simple_method_object_append(self, node, args, is_unbound_method):
        # X.append() is almost always referring to a list
        if len(args) != 2:
            return node

        return ExprNodes.PythonCapiCallNode(
            node.pos, "__Pyx_PyObject_Append", self.PyObject_Append_func_type,
            args = args,
            is_temp = node.is_temp,
            utility_code = append_utility_code
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
        # X.pop([n]) is almost always referring to a list
        if len(args) == 1:
            return ExprNodes.PythonCapiCallNode(
                node.pos, "__Pyx_PyObject_Pop", self.PyObject_Pop_func_type,
                args = args,
                is_temp = node.is_temp,
                utility_code = pop_utility_code
                )
        elif len(args) == 2:
            if isinstance(args[1], ExprNodes.CoerceToPyTypeNode) and args[1].arg.type.is_int:
                original_type = args[1].arg.type
                if PyrexTypes.widest_numeric_type(original_type, PyrexTypes.c_py_ssize_t_type) == PyrexTypes.c_py_ssize_t_type:
                    args[1] = args[1].arg
                    return ExprNodes.PythonCapiCallNode(
                        node.pos, "__Pyx_PyObject_PopIndex", self.PyObject_PopIndex_func_type,
                        args = args,
                        is_temp = node.is_temp,
                        utility_code = pop_index_utility_code
                        )
                
        return node

    PyList_Append_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_int_type, [
            PyrexTypes.CFuncTypeArg("list", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("item", PyrexTypes.py_object_type, None),
            ],
        exception_value = "-1")

    def _handle_simple_method_list_append(self, node, args, is_unbound_method):
        if len(args) != 2:
            self._error_wrong_arg_count('list.append', node, args, 2)
            return node
        return self._substitute_method_call(
            node, "PyList_Append", self.PyList_Append_func_type,
            'append', is_unbound_method, args)

    single_param_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_int_type, [
            PyrexTypes.CFuncTypeArg("obj", PyrexTypes.py_object_type, None),
            ],
        exception_value = "-1")

    def _handle_simple_method_list_sort(self, node, args, is_unbound_method):
        if len(args) != 1:
            return node
        return self._substitute_method_call(
            node, "PyList_Sort", self.single_param_func_type,
            'sort', is_unbound_method, args)

    def _handle_simple_method_list_reverse(self, node, args, is_unbound_method):
        if len(args) != 1:
            self._error_wrong_arg_count('list.reverse', node, args, 1)
            return node
        return self._substitute_method_call(
            node, "PyList_Reverse", self.single_param_func_type,
            'reverse', is_unbound_method, args)

    PyUnicode_AsEncodedString_func_type = PyrexTypes.CFuncType(
        Builtin.bytes_type, [
            PyrexTypes.CFuncTypeArg("obj", Builtin.unicode_type, None),
            PyrexTypes.CFuncTypeArg("encoding", PyrexTypes.c_char_ptr_type, None),
            PyrexTypes.CFuncTypeArg("errors", PyrexTypes.c_char_ptr_type, None),
            ],
        exception_value = "NULL")

    PyUnicode_AsXyzString_func_type = PyrexTypes.CFuncType(
        Builtin.bytes_type, [
            PyrexTypes.CFuncTypeArg("obj", Builtin.unicode_type, None),
            ],
        exception_value = "NULL")

    _special_encodings = ['UTF8', 'UTF16', 'Latin1', 'ASCII',
                          'unicode_escape', 'raw_unicode_escape']

    _special_codecs = [ (name, codecs.getencoder(name))
                        for name in _special_encodings ]

    def _handle_simple_method_unicode_encode(self, node, args, is_unbound_method):
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
            ],
        exception_value = "NULL")

    PyUnicode_Decode_func_type = PyrexTypes.CFuncType(
        Builtin.unicode_type, [
            PyrexTypes.CFuncTypeArg("string", PyrexTypes.c_char_ptr_type, None),
            PyrexTypes.CFuncTypeArg("size", PyrexTypes.c_py_ssize_t_type, None),
            PyrexTypes.CFuncTypeArg("encoding", PyrexTypes.c_char_ptr_type, None),
            PyrexTypes.CFuncTypeArg("errors", PyrexTypes.c_char_ptr_type, None),
            ],
        exception_value = "NULL")

    def _handle_simple_method_bytes_decode(self, node, args, is_unbound_method):
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
                    start = start.coerce_to(PyrexTypes.c_py_ssize_t_type, self.env_stack[-1])
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
                stop = stop.coerce_to(PyrexTypes.c_py_ssize_t_type, self.env_stack[-1])
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
                    utility_code = include_string_h_utility_code,
                    ).coerce_to(PyrexTypes.c_py_ssize_t_type, self.env_stack[-1])
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
        encoding_node = args[1]
        if isinstance(encoding_node, ExprNodes.CoerceToPyTypeNode):
            encoding_node = encoding_node.arg
        if isinstance(encoding_node, (ExprNodes.UnicodeNode, ExprNodes.StringNode,
                                      ExprNodes.BytesNode)):
            encoding = encoding_node.value
            encoding_node = ExprNodes.BytesNode(encoding_node.pos, value=encoding,
                                                 type=PyrexTypes.c_char_ptr_type)
        elif encoding_node.type.is_string:
            encoding = None
        else:
            return None

        null_node = ExprNodes.NullNode(pos)
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
            elif error_handling_node.type.is_string:
                error_handling = None
            else:
                return None
        else:
            error_handling = 'strict'
            error_handling_node = null_node

        return (encoding, encoding_node, error_handling, error_handling_node)

    def _substitute_method_call(self, node, name, func_type,
                                attr_name, is_unbound_method, args=()):
        args = list(args)
        if args:
            self_arg = args[0]
            if is_unbound_method:
                self_arg = ExprNodes.NoneCheckNode(
                    self_arg, "PyExc_TypeError",
                    "descriptor '%s' requires a '%s' object but received a 'NoneType'" % (
                    attr_name, node.function.obj.name))
            else:
                self_arg = ExprNodes.NoneCheckNode(
                    self_arg, "PyExc_AttributeError",
                    "'NoneType' object has no attribute '%s'" % attr_name)
            args[0] = self_arg
        return ExprNodes.PythonCapiCallNode(
            node.pos, name, func_type,
            args = args,
            is_temp = node.is_temp
            )


append_utility_code = UtilityCode(
proto = """
static CYTHON_INLINE PyObject* __Pyx_PyObject_Append(PyObject* L, PyObject* x) {
    if (likely(PyList_CheckExact(L))) {
        if (PyList_Append(L, x) < 0) return NULL;
        Py_INCREF(Py_None);
        return Py_None; /* this is just to have an accurate signature */
    }
    else {
        PyObject *r, *m;
        m = __Pyx_GetAttrString(L, "append");
        if (!m) return NULL;
        r = PyObject_CallFunctionObjArgs(m, x, NULL);
        Py_DECREF(m);
        return r;
    }
}
""",
impl = ""
)


pop_utility_code = UtilityCode(
proto = """
static CYTHON_INLINE PyObject* __Pyx_PyObject_Pop(PyObject* L) {
    if (likely(PyList_CheckExact(L))
            /* Check that both the size is positive and no reallocation shrinking needs to be done. */
            && likely(PyList_GET_SIZE(L) > (((PyListObject*)L)->allocated >> 1))) {
        Py_SIZE(L) -= 1;
        return PyList_GET_ITEM(L, PyList_GET_SIZE(L));
    }
    else {
        PyObject *r, *m;
        m = __Pyx_GetAttrString(L, "pop");
        if (!m) return NULL;
        r = PyObject_CallObject(m, NULL);
        Py_DECREF(m);
        return r;
    }
}
""",
impl = ""
)

pop_index_utility_code = UtilityCode(
proto = """
static PyObject* __Pyx_PyObject_PopIndex(PyObject* L, Py_ssize_t ix);
""",
impl = """
static PyObject* __Pyx_PyObject_PopIndex(PyObject* L, Py_ssize_t ix) {
    PyObject *r, *m, *t, *py_ix;
    if (likely(PyList_CheckExact(L))) {
        Py_ssize_t size = PyList_GET_SIZE(L);
        if (likely(size > (((PyListObject*)L)->allocated >> 1))) {
            if (ix < 0) {
                ix += size;
            }
            if (likely(0 <= ix && ix < size)) {
                Py_ssize_t i;
                PyObject* v = PyList_GET_ITEM(L, ix);
                Py_SIZE(L) -= 1;
                size -= 1;
                for(i=ix; i<size; i++) {
                    PyList_SET_ITEM(L, i, PyList_GET_ITEM(L, i+1));
                }
                return v;
            }
        }
    }
    py_ix = t = NULL;
    m = __Pyx_GetAttrString(L, "pop");
    if (!m) goto bad;
    py_ix = PyInt_FromSsize_t(ix);
    if (!py_ix) goto bad;
    t = PyTuple_New(1);
    if (!t) goto bad;
    PyTuple_SET_ITEM(t, 0, py_ix);
    py_ix = NULL;
    r = PyObject_CallObject(m, t);
    Py_DECREF(m);
    Py_DECREF(t);
    return r;
bad:
    Py_XDECREF(m);
    Py_XDECREF(t);
    Py_XDECREF(py_ix);
    return NULL;
}
"""
)


pyobject_as_double_utility_code = UtilityCode(
proto = '''
static double __Pyx__PyObject_AsDouble(PyObject* obj); /* proto */

#define __Pyx_PyObject_AsDouble(obj) \\
    ((likely(PyFloat_CheckExact(obj))) ? \\
     PyFloat_AS_DOUBLE(obj) : __Pyx__PyObject_AsDouble(obj))
''',
impl='''
static double __Pyx__PyObject_AsDouble(PyObject* obj) {
    PyObject* float_value;
    if (Py_TYPE(obj)->tp_as_number && Py_TYPE(obj)->tp_as_number->nb_float) {
        return PyFloat_AsDouble(obj);
    } else if (PyUnicode_CheckExact(obj) || PyBytes_CheckExact(obj)) {
#if PY_MAJOR_VERSION >= 3
        float_value = PyFloat_FromString(obj);
#else
        float_value = PyFloat_FromString(obj, 0);
#endif
    } else {
        PyObject* args = PyTuple_New(1);
        if (unlikely(!args)) goto bad;
        PyTuple_SET_ITEM(args, 0, obj);
        float_value = PyObject_Call((PyObject*)&PyFloat_Type, args, 0);
        PyTuple_SET_ITEM(args, 0, 0);
        Py_DECREF(args);
    }
    if (likely(float_value)) {
        double value = PyFloat_AS_DOUBLE(float_value);
        Py_DECREF(float_value);
        return value;
    }
bad:
    return (double)-1;
}
'''
)


include_string_h_utility_code = UtilityCode(
proto = """
#include <string.h>
"""
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
    """
    def _calculate_const(self, node):
        if node.constant_result is not ExprNodes.constant_value_not_set:
            return

        # make sure we always set the value
        not_a_constant = ExprNodes.not_a_constant
        node.constant_result = not_a_constant

        # check if all children are constant
        children = self.visitchildren(node)
        for child_result in children.itervalues():
            if type(child_result) is list:
                for child in child_result:
                    if child.constant_result is not_a_constant:
                        return
            elif child_result.constant_result is not_a_constant:
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

    NODE_TYPE_ORDER = (ExprNodes.CharNode, ExprNodes.IntNode,
                       ExprNodes.LongNode, ExprNodes.FloatNode)

    def _widest_node_class(self, *nodes):
        try:
            return self.NODE_TYPE_ORDER[
                max(map(self.NODE_TYPE_ORDER.index, map(type, nodes)))]
        except ValueError:
            return None

    def visit_ExprNode(self, node):
        self._calculate_const(node)
        return node

    def visit_BinopNode(self, node):
        self._calculate_const(node)
        if node.constant_result is ExprNodes.not_a_constant:
            return node
        if isinstance(node.constant_result, float):
            # We calculate float constants to make them available to
            # the compiler, but we do not aggregate them into a
            # constant node to prevent any loss of precision.
            return node
        if not node.operand1.is_literal or not node.operand2.is_literal:
            # We calculate other constants to make them available to
            # the compiler, but we only aggregate constant nodes
            # recursively, so non-const nodes are straight out.
            return node

        # now inject a new constant node with the calculated value
        try:
            type1, type2 = node.operand1.type, node.operand2.type
            if type1 is None or type2 is None:
                return node
        except AttributeError:
            return node

        if type1 is type2:
            new_node = node.operand1
        else:
            widest_type = PyrexTypes.widest_numeric_type(type1, type2)
            if type(node.operand1) is type(node.operand2):
                new_node = node.operand1
                new_node.type = widest_type
            elif type1 is widest_type:
                new_node = node.operand1
            elif type2 is widest_type:
                new_node = node.operand2
            else:
                target_class = self._widest_node_class(
                    node.operand1, node.operand2)
                if target_class is None:
                    return node
                new_node = target_class(pos=node.pos, type = widest_type)

        new_node.constant_result = node.constant_result
        new_node.value = str(node.constant_result)
        #new_node = new_node.coerce_to(node.type, self.current_scope)
        return new_node

    # in the future, other nodes can have their own handler method here
    # that can replace them with a constant result node

    visit_Node = Visitor.VisitorTransform.recurse_to_children


class FinalOptimizePhase(Visitor.CythonTransform):
    """
    This visitor handles several commuting optimizations, and is run
    just before the C code generation phase. 
    
    The optimizations currently implemented in this class are: 
        - Eliminate None assignment and refcounting for first assignment. 
        - isinstance -> typecheck for cdef types
    """
    def visit_SingleAssignmentNode(self, node):
        """Avoid redundant initialisation of local variables before their
        first assignment.
        """
        self.visitchildren(node)
        if node.first:
            lhs = node.lhs
            lhs.lhs_of_first_assignment = True
            if isinstance(lhs, ExprNodes.NameNode) and lhs.entry.type.is_pyobject:
                # Have variable initialized to 0 rather than None
                lhs.entry.init_to_none = False
                lhs.entry.init = 0
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
                    from CythonScope import utility_scope
                    node.function.entry = utility_scope.lookup('PyObject_TypeCheck')
                    node.function.type = node.function.entry.type
                    PyTypeObjectPtr = PyrexTypes.CPtrType(utility_scope.lookup('PyTypeObject').type)
                    node.args[1] = ExprNodes.CastNode(node.args[1], PyTypeObjectPtr)
        return node
