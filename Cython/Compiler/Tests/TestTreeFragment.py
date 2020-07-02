from Cython.TestUtils import CythonTest
from Cython.Compiler.TreeFragment import *
from Cython.Compiler.Nodes import *
from Cython.Compiler.UtilNodes import *
from Cython.Compiler.Errors import local_errors
import Cython.Compiler.Naming as Naming

class TestTreeFragments(CythonTest):

    def test_basic(self):
        F = self.fragment(u"x = 4")
        T = F.copy()
        self.assertCode(u"x = 4", T)

    def test_copy_is_taken(self):
        F = self.fragment(u"if True: x = 4")
        T1 = F.root
        T2 = F.copy()
        self.assertEqual("x", T2.stats[0].if_clauses[0].body.lhs.name)
        T2.stats[0].if_clauses[0].body.lhs.name = "other"
        self.assertEqual("x", T1.stats[0].if_clauses[0].body.lhs.name)

    def test_substitutions_are_copied(self):
        T = self.fragment(u"y + y").substitute({"y": NameNode(pos=None, name="x")})
        self.assertEqual("x", T.stats[0].expr.operand1.name)
        self.assertEqual("x", T.stats[0].expr.operand2.name)
        self.assertTrue(T.stats[0].expr.operand1 is not T.stats[0].expr.operand2)

    def test_substitution(self):
        F = self.fragment(u"x = 4")
        y = NameNode(pos=None, name=u"y")
        T = F.substitute({"x" : y})
        self.assertCode(u"y = 4", T)

    def test_exprstat(self):
        F = self.fragment(u"PASS")
        pass_stat = PassStatNode(pos=None)
        T = F.substitute({"PASS" : pass_stat})
        self.assertTrue(isinstance(T.stats[0], PassStatNode), T)

    def test_pos_is_transferred(self):
        F = self.fragment(u"""
        x = y
        x = u * v ** w
        """)
        T = F.substitute({"v" : NameNode(pos=None, name="a")})
        v = F.root.stats[1].rhs.operand2.operand1
        a = T.stats[1].rhs.operand2.operand1
        self.assertEqual(v.pos, a.pos)

    def test_temps(self):
        TemplateTransform.temp_name_counter = 0
        F = self.fragment(u"""
            TMP
            x = TMP
        """)
        T = F.substitute(temps=[u"TMP"])
        s = T.body.stats
        self.assertTrue(isinstance(s[0].expr, TempRefNode))
        self.assertTrue(isinstance(s[1].rhs, TempRefNode))
        self.assertTrue(s[0].expr.handle is s[1].rhs.handle)

    def test_parse_fault_tolerant_complete(self):
        code = u'''
def method():
    pass

def method2():
    error_here =

def method3():
    error_here.

def method4():
    without_error = 10

def method5():
    error_here =
'''
        with local_errors() as errors:
            stats = parse_from_strings("test_name", code, fault_tolerant=True).body.stats
        self.assertEquals(len(stats), 5)
        self.assertIsInstance(stats[0], DefNode)
        self.assertEqual(str(stats[0].name), "method")
        self.assertIsInstance(stats[0].body, PassStatNode)
        self.assertIsInstance(stats[1], DefNode)
        self.assertEqual(str(stats[1].name), "method2")
        self.assertIsInstance(stats[1].body, PassStatNode)
        self.assertIsInstance(stats[2], DefNode)
        self.assertEqual(str(stats[2].name), "method3")
        self.assertIsInstance(stats[2].body, ExprStatNode)
        self.assertIsInstance(stats[3], DefNode)
        self.assertEqual(str(stats[3].name), "method4")
        self.assertIsInstance(stats[3].body, SingleAssignmentNode)
        self.assertIsInstance(stats[4], DefNode)
        self.assertEqual(str(stats[4].name), "method5")
        self.assertIsInstance(stats[4].body, PassStatNode)
        self.assertEquals(len(errors), 5)
        self.assertEqual(
            "CompileError((<StringSourceDescriptor:test_name>, 6, 16), 'Expected an identifier or literal')",
            repr(errors[0])
        )
        self.assertEqual(
            "CompileError((<StringSourceDescriptor:test_name>, 6, 4), \"Internal Error: 'NoneType' object has no attribute 'pos'\")",
            repr(errors[1])
        )
        self.assertEqual(
            "CompileError((<StringSourceDescriptor:test_name>, 9, 15), 'Expected an identifier')",
            repr(errors[2])
        )
        self.assertEqual(
            "CompileError((<StringSourceDescriptor:test_name>, 15, 16), 'Expected an identifier or literal')",
            repr(errors[3])
        )
        self.assertEqual(
            "CompileError((<StringSourceDescriptor:test_name>, 15, 4), \"Internal Error: 'NoneType' object has no attribute 'pos'\")",
            repr(errors[4])
        )

if __name__ == "__main__":
    import unittest
    unittest.main()
