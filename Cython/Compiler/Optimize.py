import Nodes
import ExprNodes
import PyrexTypes
import Visitor

def unwrap_node(node):
    while isinstance(node, ExprNodes.PersistentNode):
        node = node.arg
    return node

def is_common_value(a, b):
    a = unwrap_node(a)
    b = unwrap_node(b)
    if isinstance(a, ExprNodes.NameNode) and isinstance(b, ExprNodes.NameNode):
        return a.name == b.name
    if isinstance(a, ExprNodes.AttributeNode) and isinstance(b, ExprNodes.AttributeNode):
        return not a.is_py_attr and is_common_value(a.obj, b.obj)
    return False


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
                elif hasattr(cond.operand2, 'entry') and cond.operand2.entry.is_const:
                    return cond.operand1, [cond.operand2]
            if is_common_value(cond.operand2, cond.operand2):
                if isinstance(cond.operand1, ExprNodes.ConstNode):
                    return cond.operand2, [cond.operand1]
                elif hasattr(cond.operand1, 'entry') and cond.operand1.entry.is_const:
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
        if len(node.if_clauses) < 3:
            return node
        common_var = None
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
                cases.append(Nodes.SwitchCaseNode(pos = if_clause.pos,
                                                  conditions = conditions,
                                                  body = if_clause.body))
        
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
            else:
                lhs = ExprNodes.PersistentNode(node.operand1, len(args))
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


class OptimizeRefcounting(Visitor.CythonTransform):
    def visit_SingleAssignmentNode(self, node):
        if node.first:
            lhs = node.lhs
            if isinstance(lhs, ExprNodes.NameNode) and lhs.entry.type.is_pyobject:
                # Have variable initialized to 0 rather than None
                lhs.entry.init_to_none = False
                lhs.entry.init = 0
                # Set a flag in NameNode to skip the decref
                lhs.skip_assignment_decref = True
        return node


class ExtTypePossibleValues:
    can_be_none = True
    def copy_with(self, can_be_none=None):
        result = ExtTypePossibleValues()
        if can_be_none is not None:
            result.can_be_none = can_be_none
        return result
    def new(self):
        "Polymorphic constructor"
        return ExtTypePossibleValues()

class FindPossibleVariableValues(Visitor.CythonTransform):
    """
    Annotates NameNodes with information about the possible values
    the variable referred to can take, *at that point* in the execution.

    This is done on a best effort basis, so we can be as smart or dumb
    as we want. A do-nothing-op should always be valid.

    Each type of variable keeps a different type of "variable range"
    information.

    This information is invalid if the tree is reorganized (read:
    keep this transform late in the pipeline).

    Currently this is done:
    - Extension types gets flagged 
    """

    #
    # Manage info stack
    #
    def create_empty_knowledge(self, scope):
        knowledge = {}
        for entry in scope.entries.values():
            if entry.type.is_extension_type:
                knowledge[entry] = ExtTypePossibleValues()
        return knowledge
    
    def visit_ModuleNode(self, node):
        self.knowledge = self.create_empty_knowledge(node.scope)
        self.visitchildren(node)
        return node
    
    def visit_FuncDefNode(self, node):
        oldknow = self.knowledge
        self.knowledge = self.create_empty_knowledge(node.local_scope)
        self.visitchildren(node)
        self.knowledge = oldknow
        return node

    def visit_NameNode(self, node):
        node.possible_var_values = self.knowledge.get(node.entry, None)
        return node
    
    #
    # Conditions which restrict possible variable values
    #
    def visit_IfClauseNode(self, clause):
        def process():
            self.visitchildren(clause)
            return clause

        # we're lazy and only check in one specific easy case: single comparison with None
        # the code is a bit nasty but handling the proper cases will force through better code
        # anyway
        cond = clause.condition
        if not isinstance(cond, ExprNodes.PrimaryCmpNode): return process()
        if clause.condition.cascade is not None: return process()
        if isinstance(cond.operand1, ExprNodes.NoneNode):
            operand_checked = cond.operand2
        elif isinstance(cond.operand2, ExprNodes.NoneNode):
            operand_checked = cond.operand1
        else:
            return process()
        if not isinstance(operand_checked, ExprNodes.NameNode):
            return process()
        entry = operand_checked.entry
        if entry not in self.knowledge:
            # Not tracking this variable
            return process()
        # Finally!
        if cond.operator == 'is_not':
            # Within this block we can assume the variable is not None
            # (until it is reassigned)
            self.visitchildren(clause, attrs=["condition"])
            oldvalues = self.knowledge[entry]
            self.knowledge[entry] = oldvalues.copy_with(can_be_none=False)
            self.visitchildren(clause, attrs=["body"])
            self.knowledge[entry] = oldvalues
            return clause
        else:
            return process()
            

    # Assignments which reset possible variable values
    def visit_SingleAssignmentNode(self, node):
        if isinstance(node.lhs, ExprNodes.NameNode):
            entry = node.lhs.entry
            if entry in self.knowledge:
                self.knowledge[entry] = self.knowledge[entry].new()
        self.visitchildren(node)
        return node

class OptimizeNoneChecking(Visitor.CythonTransform):
    def visit_AttributeNode(self, node):
        if isinstance(node.obj, ExprNodes.NameNode):
            obj = node.obj
            if obj.type.is_extension_type and not obj.possible_var_values.can_be_none:
                node.needs_none_check = False
        self.visitchildren(node)
        return node

                
