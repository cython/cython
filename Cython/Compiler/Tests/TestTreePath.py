import unittest
from Cython.Compiler.Visitor import PrintTree
from Cython.TestUtils import TransformTest
from Cython.Compiler.TreePath import find_first, find_all

class TestTreePath(TransformTest):

    def test_node_path(self):
        t = self.run_pipeline([], u"""
        def decorator(fun):  # DefNode
            return fun       # ReturnStatNode, NameNode
        @decorator           # NameNode
        def decorated():     # DefNode
            pass
        """)

        self.assertEquals(2, len(find_all(t, "//DefNode")))
        self.assertEquals(2, len(find_all(t, "//NameNode")))
        self.assertEquals(1, len(find_all(t, "//ReturnStatNode")))
        self.assertEquals(1, len(find_all(t, "//DefNode//ReturnStatNode")))

    def test_node_path_child(self):
        t = self.run_pipeline([], u"""
        def decorator(fun):  # DefNode
            return fun       # ReturnStatNode, NameNode
        @decorator           # NameNode
        def decorated():     # DefNode
            pass
        """)

        self.assertEquals(1, len(find_all(t, "//DefNode/ReturnStatNode/NameNode")))
        self.assertEquals(1, len(find_all(t, "//ReturnStatNode/NameNode")))

    def test_node_path_attribute_exists(self):
        t = self.run_pipeline([], u"""
        def decorator(fun):
            return fun
        @decorator
        def decorated():
            pass
        """)

        self.assertEquals(2, len(find_all(t, "//NameNode[@name]")))

    def test_node_path_attribute_string_predicate(self):
        t = self.run_pipeline([], u"""
        def decorator(fun):
            return fun
        @decorator
        def decorated():
            pass
        """)

        self.assertEquals(1, len(find_all(t, "//NameNode[@name = 'decorator']")))

if __name__ == '__main__':
    unittest.main()
