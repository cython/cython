# mode: run
# tag: pure3.8, no-cpp

# copied from cpython with minimal modifications (mainly exec->cython_inline, and a few exception strings)
# This is not currently run in C++ because all the cython_inline compilations fail for reasons that are unclear
# cython: language_level=3

import unittest
import cython
from Cython.Compiler.Main import CompileError
from Cython.Build.Inline import cython_inline
import re
import sys

if cython.compiled:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

    class StdErrHider:
        def __enter__(self):
            self.old_stderr = sys.stderr
            self.new_stderr = StringIO()
            sys.stderr = self.new_stderr

            return self

        def __exit__(self, exc_type, exc_value, traceback):
            sys.stderr = self.old_stderr

        @property
        def stderr_contents(self):
            return self.new_stderr.getvalue()

    def exec(code, globals_=None, locals_=None):
        if locals_ and globals_ and (locals_ is not globals_):
            # a hacky attempt to treat as a class definition
            code = "class Cls:\n" + "\n".join(
                "    " + line for line in code.split("\n"))
        code += "\nreturn globals(), locals()"  # so we can inspect it for changes, overriding the default cython_inline behaviour
        try:
            with StdErrHider() as stderr_handler:
                try:
                    g, l = cython_inline(code, globals=globals_, locals=locals_)
                finally:
                    err_messages = stderr_handler.stderr_contents
            if globals_ is not None:
                # because Cython inline bundles everything into a function some values that
                # we'd expect to be in globals end up in locals. This isn't quite right but is
                # as close as it's possible to get to retrieving the values
                globals_.update(l)
                globals_.update(g)
        except CompileError as exc:
            raised_message = str(exc)
            if raised_message.endswith(".pyx"):
                # unhelpfully Cython sometimes raises a compile error and sometimes just raises the filename
                raised_message = []
                for line in err_messages.split("\n"):
                    # search for the two line number groups (we can't just split by ':' because Windows
                    # filenames contain ':')
                    match = re.match(r"(.+?):\d+:\d+:(.*)", line)
                    # a usable error message with be filename:line:char: message
                    if match and match.group(1).endswith(".pyx"):
                        raised_message.append(match.group(2))
                # output all the errors - we aren't worried about reproducing the exact order CPython
                # emits errors in
                raised_message = "; ".join(raised_message)
            raise SyntaxError(raised_message) from None

if sys.version_info[0] < 3:
    # some monkey patching
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp

    class FakeSubTest(object):
        def __init__(self, *args, **kwds):
            pass
        def __enter__(self):
            pass
        def __exit__(self, *args):
            pass
    unittest.TestCase.subTest = FakeSubTest

class NamedExpressionInvalidTest(unittest.TestCase):

    def test_named_expression_invalid_01(self):
        code = """x := 0"""

        with self.assertRaisesRegex(SyntaxError, "invalid syntax"):
            exec(code, {}, {})

    def test_named_expression_invalid_02(self):
        code = """x = y := 0"""

        with self.assertRaisesRegex(SyntaxError, "invalid syntax"):
            exec(code, {}, {})

    def test_named_expression_invalid_03(self):
        code = """y := f(x)"""

        with self.assertRaisesRegex(SyntaxError, "invalid syntax"):
            exec(code, {}, {})

    def test_named_expression_invalid_04(self):
        code = """y0 = y1 := f(x)"""

        with self.assertRaisesRegex(SyntaxError, "invalid syntax"):
            exec(code, {}, {})

    def test_named_expression_invalid_06(self):
        code = """((a, b) := (1, 2))"""

        # TODO Cython correctly generates an error but the message could be better
        with self.assertRaisesRegex(SyntaxError, ""):
            exec(code, {}, {})

    def test_named_expression_invalid_07(self):
        code = """def spam(a = b := 42): pass"""

        with self.assertRaisesRegex(SyntaxError, "invalid syntax"):
            exec(code, {}, {})

    def test_named_expression_invalid_08(self):
        code = """def spam(a: b := 42 = 5): pass"""

        with self.assertRaisesRegex(SyntaxError, "invalid syntax"):
            exec(code, {}, {})

    def test_named_expression_invalid_09(self):
        code = """spam(a=b := 'c')"""

        with self.assertRaisesRegex(SyntaxError, "invalid syntax"):
            exec(code, {}, {})

    def test_named_expression_invalid_10(self):
        code = """spam(x = y := f(x))"""

        with self.assertRaisesRegex(SyntaxError, "invalid syntax"):
            exec(code, {}, {})

    def test_named_expression_invalid_11(self):
        code = """spam(a=1, b := 2)"""

        with self.assertRaisesRegex(SyntaxError,
            "follow.* keyword arg"):
            exec(code, {}, {})

    def test_named_expression_invalid_12(self):
        code = """spam(a=1, (b := 2))"""

        with self.assertRaisesRegex(SyntaxError,
            "follow.* keyword arg"):
            exec(code, {}, {})

    def test_named_expression_invalid_13(self):
        code = """spam(a=1, (b := 2))"""

        with self.assertRaisesRegex(SyntaxError,
            "follow.* keyword arg"):
            exec(code, {}, {})

    def test_named_expression_invalid_14(self):
        code = """(x := lambda: y := 1)"""

        with self.assertRaisesRegex(SyntaxError, "invalid syntax"):
            exec(code, {}, {})

    def test_named_expression_invalid_15(self):
        code = """(lambda: x := 1)"""

        # TODO at the moment the error message is valid, but not the same as Python
        with self.assertRaisesRegex(SyntaxError,
            ""):
            exec(code, {}, {})

    def test_named_expression_invalid_16(self):
        code = "[i + 1 for i in i := [1,2]]"

        # TODO at the moment the error message is valid, but not the same as Python
        with self.assertRaisesRegex(SyntaxError, ""):
            exec(code, {}, {})

    def test_named_expression_invalid_17(self):
        code = "[i := 0, j := 1 for i, j in [(1, 2), (3, 4)]]"

        # TODO at the moment the error message is valid, but not the same as Python
        with self.assertRaisesRegex(SyntaxError, ""):
            exec(code, {}, {})

    def test_named_expression_invalid_in_class_body(self):
        code = """class Foo():
            [(42, 1 + ((( j := i )))) for i in range(5)]
        """

        with self.assertRaisesRegex(SyntaxError,
            "assignment expression within a comprehension cannot be used in a class body"):
            exec(code, {}, {})

    def test_named_expression_invalid_rebinding_comprehension_iteration_variable(self):
        cases = [
            ("Local reuse", 'i', "[i := 0 for i in range(5)]"),
            ("Nested reuse", 'j', "[[(j := 0) for i in range(5)] for j in range(5)]"),
            ("Reuse inner loop target", 'j', "[(j := 0) for i in range(5) for j in range(5)]"),
            ("Unpacking reuse", 'i', "[i := 0 for i, j in [(0, 1)]]"),
            ("Reuse in loop condition", 'i', "[i+1 for i in range(5) if (i := 0)]"),
            ("Unreachable reuse", 'i', "[False or (i:=0) for i in range(5)]"),
            ("Unreachable nested reuse", 'i',
                "[(i, j) for i in range(5) for j in range(5) if True or (i:=10)]"),
        ]
        for case, target, code in cases:
            msg = f"assignment expression cannot rebind comprehension iteration variable '{target}'"
            with self.subTest(case=case):
                with self.assertRaisesRegex(SyntaxError, msg):
                    exec(code, {}, {})

    def test_named_expression_invalid_rebinding_comprehension_inner_loop(self):
        cases = [
            ("Inner reuse", 'j', "[i for i in range(5) if (j := 0) for j in range(5)]"),
            ("Inner unpacking reuse", 'j', "[i for i in range(5) if (j := 0) for j, k in [(0, 1)]]"),
        ]
        for case, target, code in cases:
            msg = f"comprehension inner loop cannot rebind assignment expression target '{target}'"
            with self.subTest(case=case):
                with self.assertRaisesRegex(SyntaxError, msg):
                    exec(code, {}) # Module scope
                with self.assertRaisesRegex(SyntaxError, msg):
                    exec(code, {}, {}) # Class scope
                with self.assertRaisesRegex(SyntaxError, msg):
                    exec(f"lambda: {code}", {}) # Function scope

    def test_named_expression_invalid_comprehension_iterable_expression(self):
        cases = [
            ("Top level", "[i for i in (i := range(5))]"),
            ("Inside tuple", "[i for i in (2, 3, i := range(5))]"),
            ("Inside list", "[i for i in [2, 3, i := range(5)]]"),
            ("Different name", "[i for i in (j := range(5))]"),
            ("Lambda expression", "[i for i in (lambda:(j := range(5)))()]"),
            ("Inner loop", "[i for i in range(5) for j in (i := range(5))]"),
            ("Nested comprehension", "[i for i in [j for j in (k := range(5))]]"),
            ("Nested comprehension condition", "[i for i in [j for j in range(5) if (j := True)]]"),
            ("Nested comprehension body", "[i for i in [(j := True) for j in range(5)]]"),
        ]
        msg = "assignment expression cannot be used in a comprehension iterable expression"
        for case, code in cases:
            with self.subTest(case=case):
                with self.assertRaisesRegex(SyntaxError, msg):
                    exec(code, {}) # Module scope - FIXME this test puts it in __invoke in cython_inline
                with self.assertRaisesRegex(SyntaxError, msg):
                    exec(code, {}, {}) # Class scope
                with self.assertRaisesRegex(SyntaxError, msg):
                    exec(f"lambda: {code}", {}) # Function scope


class NamedExpressionAssignmentTest(unittest.TestCase):

    def test_named_expression_assignment_01(self):
        (a := 10)

        self.assertEqual(a, 10)

    def test_named_expression_assignment_02(self):
        a = 20
        (a := a)

        self.assertEqual(a, 20)

    def test_named_expression_assignment_03(self):
        (total := 1 + 2)

        self.assertEqual(total, 3)

    def test_named_expression_assignment_04(self):
        (info := (1, 2, 3))

        self.assertEqual(info, (1, 2, 3))

    def test_named_expression_assignment_05(self):
        (x := 1, 2)

        self.assertEqual(x, 1)

    def test_named_expression_assignment_06(self):
        (z := (y := (x := 0)))

        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        self.assertEqual(z, 0)

    def test_named_expression_assignment_07(self):
        (loc := (1, 2))

        self.assertEqual(loc, (1, 2))

    def test_named_expression_assignment_08(self):
        if spam := "eggs":
            self.assertEqual(spam, "eggs")
        else: self.fail("variable was not assigned using named expression")

    def test_named_expression_assignment_09(self):
        if True and (spam := True):
            self.assertTrue(spam)
        else: self.fail("variable was not assigned using named expression")

    def test_named_expression_assignment_10(self):
        if (match := 10) == 10:
            pass
        else: self.fail("variable was not assigned using named expression")

    def test_named_expression_assignment_11(self):
        def spam(a):
            return a
        input_data = [1, 2, 3]
        res = [(x, y, x/y) for x in input_data if (y := spam(x)) > 0]

        self.assertEqual(res, [(1, 1, 1.0), (2, 2, 1.0), (3, 3, 1.0)])

    def test_named_expression_assignment_12(self):
        def spam(a):
            return a
        res = [[y := spam(x), x/y] for x in range(1, 5)]

        self.assertEqual(res, [[1, 1.0], [2, 1.0], [3, 1.0], [4, 1.0]])

    def test_named_expression_assignment_13(self):
        length = len(lines := [1, 2])

        self.assertEqual(length, 2)
        self.assertEqual(lines, [1,2])

    def test_named_expression_assignment_14(self):
        """
        Where all variables are positive integers, and a is at least as large
        as the n'th root of x, this algorithm returns the floor of the n'th
        root of x (and roughly doubling the number of accurate bits per
        iteration):
        """
        a = 9
        n = 2
        x = 3

        while a > (d := x // a**(n-1)):
            a = ((n-1)*a + d) // n

        self.assertEqual(a, 1)

    def test_named_expression_assignment_15(self):
        while a := False:
            pass  # This will not run

        self.assertEqual(a, False)

    def test_named_expression_assignment_16(self):
        a, b = 1, 2
        fib = {(c := a): (a := b) + (b := a + c) - b for __ in range(6)}
        self.assertEqual(fib, {1: 2, 2: 3, 3: 5, 5: 8, 8: 13, 13: 21})


class NamedExpressionScopeTest(unittest.TestCase):

    def test_named_expression_scope_01(self):
        code = """def spam():
    (a := 5)
print(a)"""

        # FIXME for some reason the error message raised is a nonsense filename instead of "undeclared name not builtin"
        # "name .* not"):
        with self.assertRaisesRegex(SyntaxError if cython.compiled else NameError, ""):
            exec(code, {}, {})

    def test_named_expression_scope_02(self):
        total = 0
        partial_sums = [total := total + v for v in range(5)]

        self.assertEqual(partial_sums, [0, 1, 3, 6, 10])
        self.assertEqual(total, 10)

    def test_named_expression_scope_03(self):
        containsOne = any((lastNum := num) == 1 for num in [1, 2, 3])

        self.assertTrue(containsOne)
        self.assertEqual(lastNum, 1)

    def test_named_expression_scope_04(self):
        def spam(a):
            return a
        res = [[y := spam(x), x/y] for x in range(1, 5)]

        self.assertEqual(y, 4)

    def test_named_expression_scope_05(self):
        def spam(a):
            return a
        input_data = [1, 2, 3]
        res = [(x, y, x/y) for x in input_data if (y := spam(x)) > 0]

        self.assertEqual(res, [(1, 1, 1.0), (2, 2, 1.0), (3, 3, 1.0)])
        self.assertEqual(y, 3)

    def test_named_expression_scope_06(self):
        res = [[spam := i for i in range(3)] for j in range(2)]

        self.assertEqual(res, [[0, 1, 2], [0, 1, 2]])
        self.assertEqual(spam, 2)

    def test_named_expression_scope_07(self):
        len(lines := [1, 2])

        self.assertEqual(lines, [1, 2])

    def test_named_expression_scope_08(self):
        def spam(a):
            return a

        def eggs(b):
            return b * 2

        res = [spam(a := eggs(b := h)) for h in range(2)]

        self.assertEqual(res, [0, 2])
        self.assertEqual(a, 2)
        self.assertEqual(b, 1)

    def test_named_expression_scope_09(self):
        def spam(a):
            return a

        def eggs(b):
            return b * 2

        res = [spam(a := eggs(a := h)) for h in range(2)]

        self.assertEqual(res, [0, 2])
        self.assertEqual(a, 2)

    def test_named_expression_scope_10(self):
        res = [b := [a := 1 for i in range(2)] for j in range(2)]

        self.assertEqual(res, [[1, 1], [1, 1]])
        self.assertEqual(a, 1)
        self.assertEqual(b, [1, 1])

    def test_named_expression_scope_11(self):
        res = [j := i for i in range(5)]

        self.assertEqual(res, [0, 1, 2, 3, 4])
        self.assertEqual(j, 4)

    def test_named_expression_scope_17(self):
        b = 0
        res = [b := i + b for i in range(5)]

        self.assertEqual(res, [0, 1, 3, 6, 10])
        self.assertEqual(b, 10)

    def test_named_expression_scope_18(self):
        def spam(a):
            return a

        res = spam(b := 2)

        self.assertEqual(res, 2)
        self.assertEqual(b, 2)

    def test_named_expression_scope_19(self):
        def spam(a):
            return a

        res = spam((b := 2))

        self.assertEqual(res, 2)
        self.assertEqual(b, 2)

    def test_named_expression_scope_20(self):
        def spam(a):
            return a

        res = spam(a=(b := 2))

        self.assertEqual(res, 2)
        self.assertEqual(b, 2)

    def test_named_expression_scope_21(self):
        def spam(a, b):
            return a + b

        res = spam(c := 2, b=1)

        self.assertEqual(res, 3)
        self.assertEqual(c, 2)

    def test_named_expression_scope_22(self):
        def spam(a, b):
            return a + b

        res = spam((c := 2), b=1)

        self.assertEqual(res, 3)
        self.assertEqual(c, 2)

    def test_named_expression_scope_23(self):
        def spam(a, b):
            return a + b

        res = spam(b=(c := 2), a=1)

        self.assertEqual(res, 3)
        self.assertEqual(c, 2)

    def test_named_expression_scope_24(self):
        a = 10
        def spam():
            nonlocal a
            (a := 20)
        spam()

        self.assertEqual(a, 20)

    def test_named_expression_scope_25(self):
        ns = {}
        code = """a = 10
def spam():
    global a
    (a := 20)
spam()"""

        exec(code, ns, {})

        self.assertEqual(ns["a"], 20)

    def test_named_expression_variable_reuse_in_comprehensions(self):
        # The compiler is expected to raise syntax error for comprehension
        # iteration variables, but should be fine with rebinding of other
        # names (e.g. globals, nonlocals, other assignment expressions)

        # The cases are all defined to produce the same expected result
        # Each comprehension is checked at both function scope and module scope
        rebinding = "[x := i for i in range(3) if (x := i) or not x]"
        filter_ref = "[x := i for i in range(3) if x or not x]"
        body_ref = "[x for i in range(3) if (x := i) or not x]"
        nested_ref = "[j for i in range(3) if x or not x for j in range(3) if (x := i)][:-3]"
        cases = [
            ("Rebind global", f"x = 1; result = {rebinding}"),
            ("Rebind nonlocal", f"result, x = (lambda x=1: ({rebinding}, x))()"),
            ("Filter global", f"x = 1; result = {filter_ref}"),
            ("Filter nonlocal", f"result, x = (lambda x=1: ({filter_ref}, x))()"),
            ("Body global", f"x = 1; result = {body_ref}"),
            ("Body nonlocal", f"result, x = (lambda x=1: ({body_ref}, x))()"),
            ("Nested global", f"x = 1; result = {nested_ref}"),
            ("Nested nonlocal", f"result, x = (lambda x=1: ({nested_ref}, x))()"),
        ]
        for case, code in cases:
            with self.subTest(case=case):
                ns = {}
                exec(code, ns)
                self.assertEqual(ns["x"], 2)
                self.assertEqual(ns["result"], [0, 1, 2])

if __name__ == "__main__":
    unittest.main()
