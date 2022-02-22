# mode: run
# cython: language_level=3

import unittest
import sys


cdef class UnSupport: pass

cdef class Unpack:
    para_list = []
    def __class_getitem__(*args, **kwargs):
        Unpack.para_list.extend([args, kwargs])

cdef class Format:
    def __class_getitem__(cls, item):
        return f'{cls.__name__}[{item.__name__}]'

cdef class ExFormat(Format): pass

cdef class Override:
    def __class_getitem__(cls, item):
        return 'Should not see this'

cdef class Covered(Override):
    def __class_getitem__(cls, item):
        return f'{cls.__name__}[{item.__name__}]'

cdef class Decorated:
    @classmethod
    def __class_getitem__(cls, item):
        return f'{cls.__name__}[{item.__name__}]'

cdef class ExDecorated(Decorated): pass

cdef class Invalid1:
    def __class_getitem__(cls): pass

cdef class Invalid2:
    def __class_getitem__(cls, item1, item2): pass

cdef class Invalid3:
    cdef dict __dict__
    def __init__(self):
        self.__class_getitem__ = lambda cls, items: 'This will not work'

cdef class Invalid4:
    __class_getitem__ = "Surprise!"


class TestClassGetitem(unittest.TestCase):
    # BEGIN - Additional tests from cython
    def test_no_class_getitem(self):
        # PyPy<7.3.8 raises AttributeError on __class_getitem__
        if hasattr(sys, "pypy_version_info")  and sys.pypy_version_info < (7, 3, 8):
            err = AttributeError
        else:
            err = TypeError
        with self.assertRaises(err):
            UnSupport[int]

    # END - Additional tests from cython

    def test_class_getitem(self):
        Unpack[int, str]
        self.assertEqual(Unpack.para_list[0], (Unpack, (int, str)))
        self.assertEqual(Unpack.para_list[1], {})

    def test_class_getitem_format(self):
        self.assertEqual(Format[int], 'Format[int]')
        self.assertEqual(Format[Format], 'Format[Format]')

    def test_class_getitem_inheritance(self):
        self.assertEqual(ExFormat[int], 'ExFormat[int]')
        self.assertEqual(ExFormat[ExFormat], 'ExFormat[ExFormat]')

    def test_class_getitem_inheritance_2(self):
        self.assertEqual(Covered[int], 'Covered[int]')
        self.assertEqual(Covered[Covered], 'Covered[Covered]')

    def test_class_getitem_classmethod(self):
        self.assertEqual(ExDecorated[int], 'ExDecorated[int]')
        self.assertEqual(ExDecorated[ExDecorated], 'ExDecorated[ExDecorated]')

    def test_class_getitem_errors(self):
        with self.assertRaises(TypeError):
            Invalid1[int]
        with self.assertRaises(TypeError):
            Invalid2[int]

    def test_class_getitem_errors_2(self):
        with self.assertRaises(TypeError):
            Format()[int]
        with self.assertRaises(TypeError):
            Invalid3()[int]
        with self.assertRaises(TypeError):
            Invalid4[int]


if __name__ == '__main__':
    unittest.main()
