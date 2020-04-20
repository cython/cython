# mode: run
# tag: pure3.7
# cython: language_level=3

# COPIED FROM CPython 3.7

import unittest
import sys


class TestClassGetitem(unittest.TestCase):
    # BEGIN - Additional tests from cython
    def test_no_class_getitem(self):
        class C: ...
        with self.assertRaises(TypeError):
            C[int]

    # END - Additional tests from cython

    def test_class_getitem(self):
        getitem_args = []
        class C:
            def __class_getitem__(*args, **kwargs):
                getitem_args.extend([args, kwargs])
                return None
        C[int, str]
        self.assertEqual(getitem_args[0], (C, (int, str)))
        self.assertEqual(getitem_args[1], {})

    def test_class_getitem_format(self):
        class C:
            def __class_getitem__(cls, item):
                return f'C[{item.__name__}]'
        self.assertEqual(C[int], 'C[int]')
        self.assertEqual(C[C], 'C[C]')

    def test_class_getitem_inheritance(self):
        class C:
            def __class_getitem__(cls, item):
                return f'{cls.__name__}[{item.__name__}]'
        class D(C): ...
        self.assertEqual(D[int], 'D[int]')
        self.assertEqual(D[D], 'D[D]')

    def test_class_getitem_inheritance_2(self):
        class C:
            def __class_getitem__(cls, item):
                return 'Should not see this'
        class D(C):
            def __class_getitem__(cls, item):
                return f'{cls.__name__}[{item.__name__}]'
        self.assertEqual(D[int], 'D[int]')
        self.assertEqual(D[D], 'D[D]')

    def test_class_getitem_classmethod(self):
        class C:
            @classmethod
            def __class_getitem__(cls, item):
                return f'{cls.__name__}[{item.__name__}]'
        class D(C): ...
        self.assertEqual(D[int], 'D[int]')
        self.assertEqual(D[D], 'D[D]')

    @unittest.skipIf(sys.version_info < (3, 6), "__init_subclass__() requires Py3.6+ (PEP 487)")
    def test_class_getitem_patched(self):
        class C:
            def __init_subclass__(cls):
                def __class_getitem__(cls, item):
                    return f'{cls.__name__}[{item.__name__}]'
                cls.__class_getitem__ = classmethod(__class_getitem__)
        class D(C): ...
        self.assertEqual(D[int], 'D[int]')
        self.assertEqual(D[D], 'D[D]')

    def test_class_getitem_with_builtins(self):
        class A(dict):
            called_with = None

            def __class_getitem__(cls, item):
                cls.called_with = item
        class B(A):
            pass
        self.assertIs(B.called_with, None)
        B[int]
        self.assertIs(B.called_with, int)

    def test_class_getitem_errors(self):
        class C_too_few:
            def __class_getitem__(cls):
                return None
        with self.assertRaises(TypeError):
            C_too_few[int]
        class C_too_many:
            def __class_getitem__(cls, one, two):
                return None
        with self.assertRaises(TypeError):
            C_too_many[int]

    def test_class_getitem_errors_2(self):
        class C:
            def __class_getitem__(cls, item):
                return None
        with self.assertRaises(TypeError):
            C()[int]
        class E: ...
        e = E()
        e.__class_getitem__ = lambda cls, item: 'This will not work'
        with self.assertRaises(TypeError):
            e[int]
        class C_not_callable:
            __class_getitem__ = "Surprise!"
        with self.assertRaises(TypeError):
            C_not_callable[int]

    def test_class_getitem_metaclass(self):
        class Meta(type):
            def __class_getitem__(cls, item):
                return f'{cls.__name__}[{item.__name__}]'
        self.assertEqual(Meta[int], 'Meta[int]')

    def test_class_getitem_with_metaclass(self):
        class Meta(type): pass
        class C(metaclass=Meta):
            def __class_getitem__(cls, item):
                return f'{cls.__name__}[{item.__name__}]'
        self.assertEqual(C[int], 'C[int]')

    def test_class_getitem_metaclass_first(self):
        class Meta(type):
            def __getitem__(cls, item):
                return 'from metaclass'
        class C(metaclass=Meta):
            def __class_getitem__(cls, item):
                return 'from __class_getitem__'
        self.assertEqual(C[int], 'from metaclass')


if __name__ == '__main__':
    unittest.main()
