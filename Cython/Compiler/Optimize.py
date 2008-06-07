import Nodes
import ExprNodes
import Visitor


def is_common_value(a, b):
    if isinstance(a, ExprNodes.NameNode) and isinstance(b, ExprNodes.NameNode):
        return a.name == b.name
    if isinstance(a, ExprNodes.AttributeNode) and isinstance(b, ExprNodes.AttributeNode):
        return not a.is_py_attr and is_common_value(a.obj, b.obj)
    return False


class SwitchTransformVisitor(Visitor.VisitorTransform):

    def extract_conditions(self, cond):
    
        if isinstance(cond, ExprNodes.CoerceToTempNode):
            cond = cond.arg
        
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
        
    def is_common_value(self, a, b):
        if isinstance(a, ExprNodes.NameNode) and isinstance(b, ExprNodes.NameNode):
            return a.name == b.name
        if isinstance(a, ExprNodes.AttributeNode) and isinstance(b, ExprNodes.AttributeNode):
            return not a.is_py_attr and is_common_value(a.obj, b.obj)
        return False
    
    def visit_IfStatNode(self, node):
        if len(node.if_clauses) < 3:
            return node
        common_var = None
        cases = []
        for if_clause in node.if_clauses:
            var, conditions = self.extract_conditions(if_clause.condition)
            if var is None:
                return node
            elif common_var is not None and not self.is_common_value(var, common_var):
                return node
            else:
                common_var = var
                cases.append(Nodes.SwitchCaseNode(pos = if_clause.pos,
                                                  conditions = conditions,
                                                  body = if_clause.body))
        return Nodes.SwitchStatNode(pos = node.pos,
                                    test = common_var,
                                    cases = cases,
                                    else_clause = node.else_clause)
                                    
    def visit_Node(self, node):
        self.visitchildren(node)
        return node
                              
