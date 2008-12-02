import Nodes
import ExprNodes
import PyrexTypes
import Visitor
import Builtin
import UtilNodes
import TypeSlots
import Symtab
from StringEncoding import EncodedString

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


class DictIterTransform(Visitor.VisitorTransform):
    """Transform a for-in-dict loop into a while loop calling PyDict_Next().
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

    def visit_ForInStatNode(self, node):
        self.visitchildren(node)
        iterator = node.iterator.sequence
        if iterator.type is Builtin.dict_type:
            # like iterating over dict.keys()
            dict_obj = iterator
            keys = True
            values = False
        else:
            if not isinstance(iterator, ExprNodes.SimpleCallNode):
                return node
            function = iterator.function
            if not isinstance(function, ExprNodes.AttributeNode):
                return node
            if function.obj.type != Builtin.dict_type:
                return node
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
                rhs = ExprNodes.IntNode(node.pos, value=0)),
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

    def visit_Node(self, node):
        self.visitchildren(node)
        return node


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


    def visit_Node(self, node):
        self.visitchildren(node)
        return node
                              

class FlattenInListTransform(Visitor.VisitorTransform):
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

        if isinstance(node.operand2, ExprNodes.TupleNode) or isinstance(node.operand2, ExprNodes.ListNode):
            args = node.operand2.args
            if len(args) == 0:
                return ExprNodes.BoolNode(pos = node.pos, value = node.operator == 'not_in')

            if node.operand1.is_temp or node.operand1.is_simple():
                lhs = node.operand1
            else:
                # FIXME: allocate temp for evaluated node.operand1
                return node

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

            return reduce(concat, conds)
        else:
            return node
        
    def visit_Node(self, node):
        self.visitchildren(node)
        return node


class FlattenBuiltinTypeCreation(Visitor.VisitorTransform):
    """Optimise some common instantiation patterns for builtin types.
    """
    def visit_GeneralCallNode(self, node):
        """Replace dict(a=b,c=d,...) by the underlying keyword dict
        construction which is done anyway.
        """
        self.visitchildren(node)
        if not node.function.type.is_builtin_type:
            return node
        if node.function.name != 'dict':
            return node
        if not isinstance(node.positional_args, ExprNodes.TupleNode):
            return node
        if len(node.positional_args.args) > 0:
            return node
        if not isinstance(node.keyword_args, ExprNodes.DictNode):
            return node
        if node.starstar_arg:
            # we could optimise this by updating the kw dict instead
            return node
        return node.keyword_args

    def visit_PyTypeTestNode(self, node):
        """Flatten redundant type checks after tree changes.
        """
        old_arg = node.arg
        self.visitchildren(node)
        if old_arg is node.arg or node.arg.type != node.type:
            return node
        return node.arg

    def visit_Node(self, node):
        self.visitchildren(node)
        return node


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
                    object_module = self.context.find_module('python_object')
                    node.function.entry = object_module.lookup('PyObject_TypeCheck')
                    if node.function.entry is None:
                        return node # only happens when there was an error earlier
                    node.function.type = node.function.entry.type
                    PyTypeObjectPtr = PyrexTypes.CPtrType(object_module.lookup('PyTypeObject').type)
                    node.args[1] = ExprNodes.CastNode(node.args[1], PyTypeObjectPtr)
        return node
