from Cython.TestUtils import CythonTest
from Cython.Compiler.TreeFragment import *
from Cython.Compiler.Nodes import *
from Cython.Compiler.UtilNodes import *
from Cython.Compiler.Errors import local_errors
import Cython.Compiler.Naming as Naming
from Cython.Compiler.ExprNodes import *


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

    def test_parse_fault_tolerant_basic(self):
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
        self.assertEqual(len(stats), 5)
        self.assertIsInstance(stats[0], DefNode)
        self.assertEqual(str(stats[0].name), "method")
        self.assertIsInstance(stats[0].body, PassStatNode)
        self.assertIsInstance(stats[1], DefNode)
        self.assertEqual(str(stats[1].name), "method2")
        self.assertIsInstance(stats[1].body, SingleAssignmentNode)
        self.assertIsInstance(stats[2], DefNode)
        self.assertEqual(str(stats[2].name), "method3")
        self.assertIsInstance(stats[2].body, ExprStatNode)
        self.assertIsInstance(stats[3], DefNode)
        self.assertEqual(str(stats[3].name), "method4")
        self.assertIsInstance(stats[3].body, SingleAssignmentNode)
        self.assertIsInstance(stats[4], DefNode)
        self.assertEqual(str(stats[4].name), "method5")
        self.assertIsInstance(stats[4].body, SingleAssignmentNode)
        self.assertTrue(len(errors) >= 3)

    def test_parse_fault_tolerant_dotted_missing(self):
        code = u'''
a.
'''
        with local_errors() as errors:
            module = parse_from_strings("test_name", code, fault_tolerant=True)
            attr_node = module.body.expr
            self.assertIsInstance(attr_node, AttributeNode)
            self.assertEqual(attr_node.obj.name, "a")
        self.assertTrue(len(errors) >= 1)

    def test_parse_fault_tolerant_class_body_missing(self):
        code = u'''
class A(
'''
        with local_errors() as errors:
            module = parse_from_strings("test_name", code, fault_tolerant=True)
            class_def = module.body
            self.assertIsInstance(class_def, PyClassDefNode)
            self.assertEqual(class_def.name, "A")
        self.assertTrue(len(errors) >= 1)

    def test_parse_fault_tolerant_method_incomplete(self):
        code = u'''
def m(
'''
        with local_errors() as errors:
            module = parse_from_strings("test_name", code, fault_tolerant=True)
            method_def = module.body
            self.assertIsInstance(method_def, DefNode)
            self.assertEqual(method_def.name, "m")
        self.assertTrue(len(errors) >= 1)

    def test_parse_fault_tolerant_method_no_body(self):
        code = u'''
def method():

'''
        with local_errors() as errors:
            module = parse_from_strings("test_name", code, fault_tolerant=True)
            method_def = module.body
            self.assertIsInstance(method_def, DefNode)
            self.assertEqual(method_def.name, "method")
        self.assertTrue(len(errors) >= 1)

    def test_parse_fault_tolerant_method_docstring_incomplete(self):
        code = u'''
def method():
    """

def method2():
    pass
'''
        with local_errors() as errors:
            module = parse_from_strings("test_name", code, fault_tolerant=True)
            method_def = module.body
            # This is not ideal (we'd like to skip the incomplete string and just
            # go to the next line), but let's go with that for now.
            self.assertIsInstance(method_def, DefNode)
            self.assertEqual(method_def.name, "method")
        self.assertTrue(len(errors) >= 1)

    def test_parse_fault_tolerant_dict_unclosed(self):
        code = u'''
my = {'a':
'''
        with local_errors() as errors:
            module = parse_from_strings("test_name", code, fault_tolerant=True)
            self.assertIsInstance(module.body, SingleAssignmentNode)
        self.assertTrue(len(errors) >= 1)

    def test_parse_fault_tolerant_dict_partial(self):
        code = u'''
my = {'a':}
'''
        with local_errors() as errors:
            module = parse_from_strings("test_name", code, fault_tolerant=True)
            self.assertIsInstance(module.body, SingleAssignmentNode)
        self.assertTrue(len(errors) >= 1)

    def test_parse_fault_tolerant_string_partial(self):
        code = u'''
my = 'a
something_else = 10
'''
        with local_errors() as errors:
            module = parse_from_strings("test_name", code, fault_tolerant=True)
            self.assertEqual(len(module.body.stats), 2)
        self.assertTrue(len(errors) >= 1)

    def test_parse_fault_tolerant_yield_missing(self):
        code = u'''
yield *
'''
        with local_errors() as errors:
            module = parse_from_strings("test_name", code, fault_tolerant=True)
            self.assertIsInstance(module.body, ExprStatNode)
        self.assertTrue(len(errors) >= 1)

        with local_errors() as errors:
            module = parse_from_strings("test_name", code, fault_tolerant=True)
            self.assertIsInstance(module.body, ExprStatNode)
        self.assertTrue(len(errors) >= 1)


if __name__ == "__main__":
    import unittest
    unittest.main()
