from Cython.TestUtils import CythonTest
from Cython.Compiler.TreeFragment import *

class TestTreeFragments(CythonTest):
    def test_basic(self):
        F = self.fragment(u"x = 4")
        T = F.copy()
        self.assertCode(u"x = 4", T)
    
    def test_copy_is_independent(self):
        F = self.fragment(u"if True: x = 4")
        T1 = F.root
        T2 = F.copy()
        self.assertEqual("x", T2.body.if_clauses[0].body.lhs.name)
        T2.body.if_clauses[0].body.lhs.name = "other"
        self.assertEqual("x", T1.body.if_clauses[0].body.lhs.name)

    def test_substitution(self):
        F = self.fragment(u"x = 4")
        y = NameNode(pos=None, name=u"y")
        T = F.substitute({"x" : y})
        self.assertCode(u"y = 4", T)

if __name__ == "__main__":
    import unittest
    unittest.main()
