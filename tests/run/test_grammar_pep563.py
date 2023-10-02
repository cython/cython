# cython: language_level=3
# The small bits of test_grammar.py that vary with the future annotations directive

from __future__ import annotations

import unittest

class GrammarTests(unittest.TestCase):

    def test_var_annot_basic_semantics(self):
        # execution order
        # FIXME for reasons that aren't really clear test_grammar.py
        # looks to have error_on_unknown_names = False set, and this
        # doesn't
        #with self.assertRaises(ZeroDivisionError):
        #    no_name[does_not_exist]: no_name_again = 1/0
        #with self.assertRaises(NameError):
        #    no_name[does_not_exist]: 1/0 = 0
        global var_annot_global

        # function semantics
        def f():
            st: str = "Hello"
            #a.b: int = (1, 2)  # FIXME
            return st
        self.assertEqual(f.__annotations__, {})
        def f_OK():
            x: 1/0
        f_OK()
        # Compile-time errors in Cython:
        """
        def fbad():
            x: int
            print(x)
        with self.assertRaises(UnboundLocalError):
            fbad()
        def f2bad():
            (no_such_global): int
            print(no_such_global)
        try:
            f2bad()
        except Exception as e:
            self.assertIs(type(e), NameError)
        """

        # class semantics
        class C:
            __foo: int
            s: str = "attr"
            z = 2
            def __init__(self, x):
                self.x: int = x

        self.assertEqual(C.__annotations__, {'_C__foo': 'int', 's': 'str'})
        #with self.assertRaises(NameError):  # FIXME
        #    class CBad:
        #        no_such_name_defined.attr: int = 0
        with self.assertRaises(NameError):
            class Cbad2(C):
                x: int
                x.y: list = []

    def test_funcdef(self):
        # argument annotation tests
        def f(x) -> list: pass
        self.assertEqual(f.__annotations__, {'return': 'list'})
        def f(x: int): pass
        self.assertEqual(f.__annotations__, {'x': 'int'})
        def f(x: int, /): pass
        self.assertEqual(f.__annotations__, {'x': 'int'})
        def f(x: int = 34, /): pass
        self.assertEqual(f.__annotations__, {'x': 'int'})
        def f(*x: str): pass
        self.assertEqual(f.__annotations__, {'x': 'str'})
        def f(**x: float): pass
        self.assertEqual(f.__annotations__, {'x': 'float'})
        def f(x, y: 1+2): pass
        self.assertEqual(f.__annotations__, {'y': '1 + 2'})
        def f(x, y: 1+2, /): pass
        self.assertEqual(f.__annotations__, {'y': '1 + 2'})
        def f(a, b: 1, c: 2, d): pass
        self.assertEqual(f.__annotations__, {'b': '1', 'c': '2'})
        def f(a, b: 1, /, c: 2, d): pass
        self.assertEqual(f.__annotations__, {'b': '1', 'c': '2'})
        def f(a, b: 1, c: 2, d, e: 3 = 4, f=5, *g: 6): pass
        self.assertEqual(f.__annotations__,
                         {'b': '1', 'c': '2', 'e': '3', 'g': '6'})
        def f(a, b: 1, c: 2, d, e: 3 = 4, f=5, *g: 6, h: 7, i=8, j: 9 = 10,
              **k: 11) -> 12: pass
        self.assertEqual(f.__annotations__,
                         {'b': '1', 'c': '2', 'e': '3', 'g': '6', 'h': '7', 'j': '9',
                          'k': '11', 'return': '12'})
        # FIXME: compile failure on positional-only argument declaration
        """
        def f(a, b: 1, c: 2, d, e: 3 = 4, f: int = 5, /, *g: 6, h: 7, i=8, j: 9 = 10,
              **k: 11) -> 12: pass
        self.assertEqual(f.__annotations__,
                          {'b': 1, 'c': 2, 'e': 3, 'f': int, 'g': 6, 'h': 7, 'j': 9,
                           'k': 11, 'return': 12})
        """
        # Check for issue #20625 -- annotations mangling
        class Spam:
            def f(self, *, __kw: 1):
                pass
        class Ham(Spam): pass
        # FIXME: not currently mangled
        """
        self.assertEqual(Spam.f.__annotations__, {'_Spam__kw': '1'})
        self.assertEqual(Ham.f.__annotations__, {'_Spam__kw': '1'})
        """
        # Check for SF Bug #1697248 - mixing decorators and a return annotation
        def null(x): return x
        @null
        def f(x) -> list: pass
        self.assertEqual(f.__annotations__, {'return': 'list'})
