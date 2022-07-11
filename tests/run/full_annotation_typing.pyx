# mode: run
# tag: pep484, warnings

# cython: annotation_typing=full

cimport cython
from cython cimport typeof
from cpython.ref cimport PyObject

try:
    from typing import Optional
except ImportError:
    pass


def old_dict_syntax(a: list, b: "int" = 2, c: {'ctype': 'long int'} = 3, d: {'type': 'long int'} = 4) -> list:
    """
    >>> old_dict_syntax([1])
    ('list object', 'int', 'long', 'long')
    [1, 2, 3, 4]
    >>> old_dict_syntax([1], 3)
    ('list object', 'int', 'long', 'long')
    [1, 3, 3, 4]
    >>> old_dict_syntax(123)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    >>> old_dict_syntax(None)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got NoneType)
    """
    print(typeof(a), typeof(b), typeof(c), typeof(d))
    a.append(b)
    a.append(c)
    a.append(d)
    return a


def pytypes_def(a: list, b: int = 2, c: long = 3, d: float = 4.0, n: list = None, o: Optional[tuple] = ()) -> list:
    """
    >>> pytypes_def([1])
    ('list object', 'int', 'long', 'float', 'list object', 'tuple object')
    [1, 2, 3, 4.0, None, ()]
    >>> pytypes_def([1], 3)
    ('list object', 'int', 'long', 'float', 'list object', 'tuple object')
    [1, 3, 3, 4.0, None, ()]
    >>> pytypes_def([1], 3, 2, 1, [], None)
    ('list object', 'int', 'long', 'float', 'list object', 'tuple object')
    [1, 3, 2, 1.0, [], None]
    >>> pytypes_def(123)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    >>> pytypes_def(None)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got NoneType)
    """
    print(typeof(a), typeof(b), typeof(c), typeof(d), typeof(n), typeof(o))
    a.append(b)
    a.append(c)
    a.append(d)
    a.append(n)
    a.append(o)
    return a


cpdef pytypes_cpdef(a: list, b: int = 2, c: long = 3, d: float = 4.0, n: list = None, o: Optional[tuple] = ()):
    """
    >>> pytypes_cpdef([1])
    ('list object', 'int', 'long', 'float', 'list object', 'tuple object')
    [1, 2, 3, 4.0, None, ()]
    >>> pytypes_cpdef([1], 3)
    ('list object', 'int', 'long', 'float', 'list object', 'tuple object')
    [1, 3, 3, 4.0, None, ()]
    >>> pytypes_cpdef([1], 3, 2, 1, [], None)
    ('list object', 'int', 'long', 'float', 'list object', 'tuple object')
    [1, 3, 2, 1.0, [], None]
    >>> pytypes_cpdef(123)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    >>> pytypes_cpdef(None)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got NoneType)
    """
    print(typeof(a), typeof(b), typeof(c), typeof(d), typeof(n), typeof(o))
    a.append(b)
    a.append(c)
    a.append(d)
    a.append(n)
    a.append(o)
    return a


cdef c_pytypes_cdef(a: list, b: int = 2, c: long = 3, d: float = 4.0, n: list = None):
    print(typeof(a), typeof(b), typeof(c), typeof(d), typeof(n))
    a.append(b)
    a.append(c)
    a.append(d)
    a.append(n)
    return a


def pytypes_cdef(a, b=2, c=3, d=4):
    """
    >>> pytypes_cdef([1])
    ('list object', 'int', 'long', 'float', 'list object')
    [1, 2, 3, 4.0, None]
    >>> pytypes_cdef([1], 3)
    ('list object', 'int', 'long', 'float', 'list object')
    [1, 3, 3, 4.0, None]
    >>> pytypes_cdef(123)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    return c_pytypes_cdef(a, b, c, d)


def ctypes_def(a: list, b: cython.int = 2, c: cython.long = 3, d: cython.float = 4) -> list:
    """
    >>> ctypes_def([1])
    ('list object', 'int', 'long', 'float')
    [1, 2, 3, 4.0]
    >>> ctypes_def([1], 3)
    ('list object', 'int', 'long', 'float')
    [1, 3, 3, 4.0]
    >>> ctypes_def(123)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    """
    print(typeof(a), typeof(b), typeof(c), typeof(d))
    a.append(b)
    a.append(c)
    a.append(d)
    return a


def return_tuple_for_carray() -> tuple:
    """
    >>> return_tuple_for_carray()
    (1, 2, 3)
    """
    cdef int[3] x
    x = [1, 2, 3]
    return x


def py_float_default(price : Optional[float]=None, ndigits=4):
    """
    Python default arguments should prevent C type inference.

    >>> py_float_default()
    (None, 4)
    >>> py_float_default(None)
    (None, 4)
    >>> py_float_default(2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...float...
    >>> py_float_default(2.0)
    (2.0, 4)
    >>> py_float_default(2, 3)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...float...
    """
    return price, ndigits


cdef class ClassAttribute:
    cls_attr1 : cython.float = 1.
    cls_attr2 : float = 1.


cdef class Attributes:
    """
    >>> inst = Attributes()
    >>> inst.x  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    AttributeError: ...
    >>> inst.get_xy()
    (5, 1.0)
    >>> inst.typeofs()
    ('int', 'float')
    """
    x: int
    y: float

    def __init__(self):
        self.x = 5
        self.y = 1.

    def typeofs(self):
        return (typeof(self.x), typeof(self.y))

    def get_xy(self):
        return self.x, self.y

mod_int: int = 1
mod_float: float
mod_float = 2.
mod_double: double = 3.
mod_dict: dict = {}

def test_globals():
    """
    >>> test_globals()
    ('int', 'float', 'double', 'dict object')
    (1, 2.0, 3.0, {})
    """
    print(typeof(mod_int), typeof(mod_float), typeof(mod_double), typeof(mod_dict))
    return mod_int, mod_float, mod_double, mod_dict


_WARNINGS = """
16:32: Strings should no longer be used for type declarations. Use 'cython.int' etc. directly.
16:47: Dicts should no longer be used as type annotations. Use 'cython.int' etc. directly.
16:56: Strings should no longer be used for type declarations. Use 'cython.int' etc. directly.
16:77: Dicts should no longer be used as type annotations. Use 'cython.int' etc. directly.
16:85: Strings should no longer be used for type declarations. Use 'cython.int' etc. directly.
38:66: PEP-484 recommends 'typing.Optional[...]' for arguments that can be None.
65:70: PEP-484 recommends 'typing.Optional[...]' for arguments that can be None.
92:70: PEP-484 recommends 'typing.Optional[...]' for arguments that can be None.
166:16: Annotation ignored since class-level attributes must be Python objects. Were you trying to set up an instance attribute?
167:16: Annotation ignored since class-level attributes must be Python objects. Were you trying to set up an instance attribute?
# BUG:
65:6: 'pytypes_cpdef' redeclared
"""
