from Cython.Compiler.Visitor import VisitorTransform
from Cython.Compiler.Nodes import *
from Cython.Compiler.TreeFragment import TreeFragment


class PostParse(VisitorTransform):
    """
    This transform fixes up a few things after parsing
    in order to make the parse tree more suitable for
    transforms.

    a) After parsing, blocks with only one statement will
    be represented by that statement, not by a StatListNode.
    When doing transforms this is annoying and inconsistent,
    as one cannot in general remove a statement in a consistent
    way and so on. This transform wraps any single statements
    in a StatListNode containing a single statement.

    b) The PassStatNode is a noop and serves no purpose beyond
    plugging such one-statement blocks; i.e., once parsed a
`    "pass" can just as well be represented using an empty
    StatListNode. This means less special cases to worry about
    in subsequent transforms (one always checks to see if a
    StatListNode has no children to see if the block is empty).
    """

    def __init__(self):
        super(PostParse, self).__init__()
        self.is_in_statlist = False
        self.is_in_expr = False

    def visit_Node(self, node):
        self.visitchildren(node)
        return node

    def visit_ExprNode(self, node):
        stacktmp = self.is_in_expr
        self.is_in_expr = True
        self.visitchildren(node)
        self.is_in_expr = stacktmp
        return node

    def visit_StatNode(self, node, is_listcontainer=False):
        stacktmp = self.is_in_statlist
        self.is_in_statlist = is_listcontainer
        self.visitchildren(node)
        self.is_in_statlist = stacktmp
        if not self.is_in_statlist and not self.is_in_expr:
            return StatListNode(pos=node.pos, stats=[node])
        else:
            return node

    def visit_PassStatNode(self, node):
        if not self.is_in_statlist:
            return StatListNode(pos=node.pos, stats=[])
        else:
            return []

    def visit_StatListNode(self, node):
        self.is_in_statlist = True
        self.visitchildren(node)
        self.is_in_statlist = False
        return node

    def visit_ParallelAssignmentNode(self, node):
        return self.visit_StatNode(node, True)
    
    def visit_CEnumDefNode(self, node):
        return self.visit_StatNode(node, True)

    def visit_CStructOrUnionDefNode(self, node):
        return self.visit_StatNode(node, True)

class WithTransform(VisitorTransform):

    template_without_target = TreeFragment(u"""
        import sys as SYS
        MGR = EXPR
        EXIT = MGR.__exit__
        MGR.__enter__()
        EXC = True
        try:
            try:
                BODY
            except:
                EXC = False
                if not EXIT(*SYS.exc_info()):
                    raise
        finally:
            if EXC:
                EXIT(None, None, None)
    """, u"WithTransformFragment")

    template_with_target = TreeFragment(u"""
        import sys as SYS
        MGR = EXPR
        EXIT = MGR.__exit__
        VALUE = MGR.__enter__()
        EXC = True
        try:
            try:
                TARGET = VALUE
                BODY
            except:
                EXC = False
                if not EXIT(*SYS.exc_info()):
                    raise
        finally:
            if EXC:
                EXIT(None, None, None)
    """, u"WithTransformFragment")

    def visit_Node(self, node):
    	self.visitchildren(node)
	return node

    def visit_WithStatNode(self, node):
        if node.target is not None:
            result = self.template_with_target.substitute({
                u'EXPR' : node.manager,
                u'BODY' : node.body,
                u'TARGET' : node.target
                }, temps=(u'MGR', u'EXC', u"EXIT", u"VALUE", u"SYS"),
                pos = node.pos)
        else:
            result = self.template_without_target.substitute({
                u'EXPR' : node.manager,
                u'BODY' : node.body,
                }, temps=(u'MGR', u'EXC', u"EXIT", u"SYS"),
                pos = node.pos)
        
        return result.body.stats


class CallExitFuncNode(Node):
    def analyse_types(self, env):
        pass
    def analyse_expressions(self, env):
        self.exc_vars = [
            env.allocate_temp(PyrexTypes.py_object_type)
            for x in xrange(3)
        ]
        
        
    def generate_result(self, code):
        code.putln("""{
        PyObject* type; PyObject* value; PyObject* tb;
        __Pyx_GetException(
        }""")
