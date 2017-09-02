# mode: run
# tag: pep484, warnings

cimport cython
from cython cimport typeof


def old_dict_syntax(a: list, b: "int" = 2, c: {'ctype': 'long int'} = 3, d: {'type': 'float'} = 4) -> list:
    """
    >>> old_dict_syntax([1])
    ('list object', 'int', 'long', 'float')
    [1, 2, 3, 4.0]
    >>> old_dict_syntax([1], 3)
    ('list object', 'int', 'long', 'float')
    [1, 3, 3, 4.0]
    >>> old_dict_syntax(123)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    """
    print(typeof(a), typeof(b), typeof(c), typeof(d))
    a.append(b)
    a.append(c)
    a.append(d)
    return a


def pytypes_def(a: list, b: int = 2, c: long = 3, d: float = 4) -> list:
    """
    >>> pytypes_def([1])
    ('list object', 'Python object', 'Python object', 'double')
    [1, 2, 3, 4.0]
    >>> pytypes_def([1], 3)
    ('list object', 'Python object', 'Python object', 'double')
    [1, 3, 3, 4.0]
    >>> pytypes_def(123)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    """
    print(typeof(a), typeof(b), typeof(c), typeof(d))
    a.append(b)
    a.append(c)
    a.append(d)
    return a


cpdef pytypes_cpdef(a: list, b: int = 2, c: long = 3, d: float = 4):
    """
    >>> pytypes_cpdef([1])
    ('list object', 'Python object', 'Python object', 'double')
    [1, 2, 3, 4.0]
    >>> pytypes_cpdef([1], 3)
    ('list object', 'Python object', 'Python object', 'double')
    [1, 3, 3, 4.0]
    >>> pytypes_cpdef(123)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    """
    print(typeof(a), typeof(b), typeof(c), typeof(d))
    a.append(b)
    a.append(c)
    a.append(d)
    return a


cdef c_pytypes_cdef(a: list, b: int = 2, c: long = 3, d: float = 4):
    print(typeof(a), typeof(b), typeof(c), typeof(d))
    a.append(b)
    a.append(c)
    a.append(d)
    return a


def pytypes_cdef(a, b=2, c=3, d=4):
    """
    >>> pytypes_cdef([1])
    ('list object', 'Python object', 'Python object', 'double')
    [1, 2, 3, 4.0]
    >>> pytypes_cdef([1], 3)
    ('list object', 'Python object', 'Python object', 'double')
    [1, 3, 3, 4.0]
    >>> pytypes_cdef(123)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    return c_pytypes_cdef(a, b, c, d)


def ctypes_def(a: list, b: cython.int = 2, c: cython.long = 3, d: cython.float = 4) -> list:
    """
    >>> pytypes_def([1])
    ('list object', 'Python object', 'Python object', 'double')
    [1, 2, 3, 4.0]
    >>> pytypes_def([1], 3)
    ('list object', 'Python object', 'Python object', 'double')
    [1, 3, 3, 4.0]
    >>> pytypes_def(123)
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


_WARNINGS = """
8:32: Strings should no longer be used for type declarations. Use 'cython.int' etc. directly.
8:47: Dicts should no longer be used as type annotations. Use 'cython.int' etc. directly.
8:56: Strings should no longer be used for type declarations. Use 'cython.int' etc. directly.
8:77: Dicts should no longer be used as type annotations. Use 'cython.int' etc. directly.
8:85: Python type declaration in signature annotation does not refer to a Python type
8:85: Strings should no longer be used for type declarations. Use 'cython.int' etc. directly.
# BUG:
46:6: 'pytypes_cpdef' redeclared
"""
