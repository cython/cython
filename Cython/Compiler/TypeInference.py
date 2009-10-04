import ExprNodes
import PyrexTypes
from Visitor import CythonTransform

class TypedExprNode(ExprNodes.ExprNode):
    # Used for declaring assignments of a specified type whithout a known entry.
    def __init__(self, type):
        self.type = type

object_expr = TypedExprNode(PyrexTypes.py_object_type)

class MarkAssignments(CythonTransform):
    
    def mark_assignment(self, lhs, rhs):
        print lhs.pos[1:]
        if isinstance(lhs, ExprNodes.NameNode):
            lhs.entry.assignments.append(rhs)
            print lhs.name, rhs
        elif isinstance(lhs, ExprNodes.SequenceNode):
            for arg in lhs.args:
                self.mark_assignment(arg, object_expr)
        else:
            # Could use this info to infer cdef class attributes...
            pass
    
    def visit_SingleAssignmentNode(self, node):
        self.mark_assignment(node.lhs, node.rhs)
        self.visitchildren(node)
        return node

    def visit_CascadedAssignmentNode(self, node):
        for lhs in node.lhs_list:
            self.mark_assignment(lhs, node.rhs)
        self.visitchildren(node)
        return node
    
    def visit_InPlaceAssignmentNode(self, node):
        self.mark_assignment(node.lhs, node.create_binop_node())
        self.visitchildren(node)
        return node

    def visit_ForInStatNode(self, node):
        # TODO: Figure out how this interacts with the range optimization...
        self.mark_assignment(node.target, object_expr)
        self.visitchildren(node)
        return node

    def visit_ForFromStatNode(self, node):
        self.mark_assignment(node.target, node.bound1)
        if node.step is not None:
            self.mark_assignment(node.target, ExprNodes.binop_node(self.pos, '+', node.bound1, node.step))
        self.visitchildren(node)
        return node

    def visit_ExceptClauseNode(self, node):
        if node.target is not None:
            self.mark_assignment(node.target, object_expr)
        self.visitchildren(node)
        return node
    
    def visit_FromCImportStatNode(self, node):
        raise NotImplementedError # Can't occur in local scopes anyways...

    def visit_FromImportStatNode(self, node):
        for name, target in node.items:
            if name != "*":
                self.mark_assignment(target, object_expr)
        self.visitchildren(node)
        return node
