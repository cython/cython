import Nodes
import ExprNodes
import PyrexTypes
import Visitor
import Builtin
import UtilNodes
import TypeSlots
import Symtab
import Options

from Code import UtilityCode
from StringEncoding import EncodedString
from Errors import error
from ParseTreeTransforms import SkipDeclarations

try:
    reduce
except NameError:
    from functools import reduce

#def unwrap_node(node):
#    while isinstance(node, ExprNodes.PersistentNode):
#        node = node.arg
#    return node

# Temporary hack while PersistentNode is out of order
def unwrap_node(node):
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
        if not isinstance(iterator, ExprNodes.SimpleCallNode):
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
        if iterator.self is None and \
               isinstance(function, ExprNodes.NameNode) and \
               function.entry.is_builtin and \
               function.name == 'enumerate':
            return self._transform_enumerate_iteration(node, iterator)

        # range() iteration?
        if Options.convert_range and node.target.type.is_int:
            if iterator.self is None and \
                    isinstance(function, ExprNodes.NameNode) and \
                    function.entry.is_builtin and \
                    function.name in ('range', 'xrange'):
                return self._transform_range_iteration(node, iterator)

        return node

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
            step.value = -step_value
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

        for_node = Nodes.ForFromStatNode(
            node.pos,
            target=node.target,
            bound1=bound1, relation1=relation1,
            relation2=relation2, bound2=bound2,
            step=step, body=node.body,
            else_clause=node.else_clause,
            from_range=True)
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
            class FakeEnv(object):
                nogil = False
            if dest_type.is_pyobject:
                if dest_type.is_extension_type or dest_type.is_builtin_type:
                    obj_node = ExprNodes.PyTypeTestNode(obj_node, dest_type, FakeEnv())
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
                return (temp_result, CoercedTempNode(dest_type, obj_node, FakeEnv()))

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
    
        if isinstance(cond, ExprNodes.CoerceToTempNode):
            cond = cond.arg

        if isinstance(cond, ExprNodes.TypecastNode):
            cond = cond.operand
    
        if (isinstance(cond, ExprNodes.PrimaryCmpNode) 
                and cond.cascade is None 
                and cond.operator == '=='
                and not cond.is_python_comparison()):
            if is_common_value(cond.operand1, cond.operand1):
                if isinstance(cond.operand2, ExprNodes.ConstNode):
                    return cond.operand1, [cond.operand2]
                elif hasattr(cond.operand2, 'entry') and cond.operand2.entry and cond.operand2.entry.is_const:
                    return cond.operand1, [cond.operand2]
            if is_common_value(cond.operand2, cond.operand2):
                if isinstance(cond.operand1, ExprNodes.ConstNode):
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


class OptimizeBuiltinCalls(Visitor.VisitorTransform):
    """Optimize some common methods calls and instantiation patterns
    for builtin types.
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
        return self._dispatch_to_handler(
            node, function, arg_tuple, node.keyword_args)

    def visit_SimpleCallNode(self, node):
        self.visitchildren(node)
        function = node.function
        if not function.type.is_pyobject:
            return node
        arg_tuple = node.arg_tuple
        if not isinstance(arg_tuple, ExprNodes.TupleNode):
            return node
        return self._dispatch_to_handler(
            node, node.function, arg_tuple)

    def visit_PyTypeTestNode(self, node):
        """Flatten redundant type checks after tree changes.
        """
        old_arg = node.arg
        self.visitchildren(node)
        if old_arg is node.arg or node.arg.type != node.type:
            return node
        return node.arg

    def _find_handler(self, match_name, has_kwargs):
        call_type = has_kwargs and 'general' or 'simple'
        handler = getattr(self, '_handle_%s_%s' % (call_type, match_name), None)
        if handler is None:
            handler = getattr(self, '_handle_any_%s' % match_name, None)
        return handler

    def _dispatch_to_handler(self, node, function, arg_tuple, kwargs=None):
        if function.is_name:
            match_name = "_function_%s" % function.name
            function_handler = self._find_handler(
                "function_%s" % function.name, kwargs)
            if function_handler is None:
                return node
            if kwargs:
                return function_handler(node, arg_tuple, kwargs)
            else:
                return function_handler(node, arg_tuple)
        elif isinstance(function, ExprNodes.AttributeNode):
            arg_list = arg_tuple.args
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
                "method_%s_%s" % (type_name, function.attribute), kwargs)
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

    ### builtin types

    def _handle_general_function_dict(self, node, pos_args, kwargs):
        """Replace dict(a=b,c=d,...) by the underlying keyword dict
        construction which is done anyway.
        """
        if len(pos_args.args) > 0:
            return node
        if not isinstance(kwargs, ExprNodes.DictNode):
            return node
        if node.starstar_arg:
            # we could optimize this by updating the kw dict instead
            return node
        return kwargs

    PyDict_Copy_func_type = PyrexTypes.CFuncType(
        Builtin.dict_type, [
            PyrexTypes.CFuncTypeArg("dict", Builtin.dict_type, None)
            ])

    def _handle_simple_function_dict(self, node, pos_args):
        """Replace dict(some_dict) by PyDict_Copy(some_dict).
        """
        if len(pos_args.args) != 1:
            return node
        dict_arg = pos_args.args[0]
        if dict_arg.type is not Builtin.dict_type:
            return node

        dict_arg = ExprNodes.NoneCheckNode(
            dict_arg, "PyExc_TypeError", "'NoneType' is not iterable")
        return ExprNodes.PythonCapiCallNode(
            node.pos, "PyDict_Copy", self.PyDict_Copy_func_type,
            args = [dict_arg],
            is_temp = node.is_temp
            )

    def _handle_simple_function_set(self, node, pos_args):
        """Replace set([a,b,...]) by a literal set {a,b,...}.
        """
        arg_count = len(pos_args.args)
        if arg_count == 0:
            return ExprNodes.SetNode(node.pos, args=[],
                                     type=Builtin.set_type, is_temp=1)
        if arg_count > 1:
            return node
        iterable = pos_args.args[0]
        if isinstance(iterable, (ExprNodes.ListNode, ExprNodes.TupleNode)):
            return ExprNodes.SetNode(node.pos, args=iterable.args,
                                     type=Builtin.set_type, is_temp=1)
        elif isinstance(iterable, ExprNodes.ComprehensionNode) and \
                iterable.type is Builtin.list_type:
            iterable.target = ExprNodes.SetNode(
                node.pos, args=[], type=Builtin.set_type, is_temp=1)
            iterable.type = Builtin.set_type
            iterable.pos = node.pos
            return iterable
        else:
            return node

    PyList_AsTuple_func_type = PyrexTypes.CFuncType(
        Builtin.tuple_type, [
            PyrexTypes.CFuncTypeArg("list", Builtin.list_type, None)
            ])

    def _handle_simple_function_tuple(self, node, pos_args):
        """Replace tuple([...]) by a call to PyList_AsTuple.
        """
        if len(pos_args.args) != 1:
            return node
        list_arg = pos_args.args[0]
        if list_arg.type is not Builtin.list_type:
            return node
        if not isinstance(list_arg, (ExprNodes.ComprehensionNode,
                                     ExprNodes.ListNode)):
            # everything else may be None => take the safe path
            return node

        return ExprNodes.PythonCapiCallNode(
            node.pos, "PyList_AsTuple", self.PyList_AsTuple_func_type,
            args = pos_args.args,
            is_temp = node.is_temp
            )

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
        # not really a builtin *type*, but worth optimising anyway
        args = pos_args.args
        if len(args) == 2:
            node = ExprNodes.PythonCapiCallNode(
                node.pos, "PyObject_GetAttr", self.PyObject_GetAttr2_func_type,
                args = args,
                is_temp = node.is_temp
                )
        elif len(args) == 3:
            node = ExprNodes.PythonCapiCallNode(
                node.pos, "__Pyx_GetAttr3", self.PyObject_GetAttr3_func_type,
                utility_code = Builtin.getattr3_utility_code,
                args = args,
                is_temp = node.is_temp
                )
        else:
            error(node.pos, "getattr() called with wrong number of args, "
                  "expected 2 or 3, found %d" % len(args))
        return node

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

    PyList_Append_func_type = PyrexTypes.CFuncType(
        PyrexTypes.c_int_type, [
            PyrexTypes.CFuncTypeArg("list", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("item", PyrexTypes.py_object_type, None),
            ],
        exception_value = "-1")

    def _handle_simple_method_list_append(self, node, args, is_unbound_method):
        if len(args) != 2:
            error(node.pos, "list.append(x) called with wrong number of args, found %d" %
                  len(args))
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
            error(node.pos, "list.reverse(x) called with wrong number of args, found %d" %
                  len(args))
            return node
        return self._substitute_method_call(
            node, "PyList_Reverse", self.single_param_func_type,
            'reverse', is_unbound_method, args)

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
        # FIXME: args[0] may need a runtime None check (ticket #166)
        return ExprNodes.PythonCapiCallNode(
            node.pos, name, func_type,
            args = args,
            is_temp = node.is_temp
            )


append_utility_code = UtilityCode(
proto = """
static INLINE PyObject* __Pyx_PyObject_Append(PyObject* L, PyObject* x) {
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
        except (ValueError, TypeError, KeyError, IndexError, AttributeError):
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
        try:
            if node.operand1.type is None or node.operand2.type is None:
                return node
        except AttributeError:
            return node

        type1, type2 = node.operand1.type, node.operand2.type
        if isinstance(node.operand1, ExprNodes.ConstNode) and \
               isinstance(node.operand1, ExprNodes.ConstNode):
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
                    new_node = target_class(type = widest_type)
        else:
            return node

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
                    cython_scope = self.context.cython_scope
                    node.function.entry = cython_scope.lookup('PyObject_TypeCheck')
                    node.function.type = node.function.entry.type
                    PyTypeObjectPtr = PyrexTypes.CPtrType(cython_scope.lookup('PyTypeObject').type)
                    node.args[1] = ExprNodes.CastNode(node.args[1], PyTypeObjectPtr)
        return node
