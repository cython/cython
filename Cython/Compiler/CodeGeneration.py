from __future__ import absolute_import

from .Visitor import VisitorTransform
from .Nodes import StatListNode


class ExtractPxdCode(VisitorTransform):
    """
    Finds nodes in a pxd file that should generate code, and
    returns them in a StatListNode.

    The result is a tuple (StatListNode, ModuleScope), i.e.
    everything that is needed from the pxd after it is processed.

    A purer approach would be to seperately compile the pxd code,
    but the result would have to be slightly more sophisticated
    than pure strings (functions + wanted interned strings +
    wanted utility code + wanted cached objects) so for now this
    approach is taken.
    """

    def __call__(self, root):
        self.code_statements = []
        self.visitchildren(root)
        return (StatListNode(root.pos, stats=self.code_statements), root.scope)

    def visit_FuncDefNode(self, node):
        self.code_statements.append(node)
        # Do not visit children, nested funcdefnodes will
        # also be moved by this action...
        return node

    def visit_Node(self, node):
        self.visitchildren(node)
        return node

    def visit_CEnumDefNode(self, node):
        if node.visibility == 'public' or node.is_overridable:
            self.code_statements.append(node)
        return node
