# cython: annotation_typing=True

from cython cimport typeof


def pytypes_def(a: list, b: "int" = 2, c: {'ctype': 'long int'} = 3, d: {'type': 'float'} = 4) -> list:
    """
    >>> pytypes_def([1])
    ('list object', 'int', 'long', 'float')
    [1, 2, 3, 4.0]
    >>> pytypes_def([1], 3)
    ('list object', 'int', 'long', 'float')
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


cpdef pytypes_cpdef(a: list, b: "int" = 2, c: {'ctype': 'long int'} = 3, d: {'type': 'float'} = 4):
    """
    >>> pytypes_cpdef([1])
    ('list object', 'int', 'long', 'float')
    [1, 2, 3, 4.0]
    >>> pytypes_cpdef([1], 3)
    ('list object', 'int', 'long', 'float')
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


cdef c_pytypes_cdef(a: list, b: "int" = 2, c: {'ctype': 'long int'} = 3, d: {'type': 'float'} = 4):
    print(typeof(a), typeof(b), typeof(c), typeof(d))
    a.append(b)
    a.append(c)
    a.append(d)
    return a


def pytypes_cdef(a, b=2, c=3, d=4):
    """
    >>> pytypes_cdef([1])
    ('list object', 'int', 'long', 'float')
    [1, 2, 3, 4.0]
    >>> pytypes_cdef([1], 3)
    ('list object', 'int', 'long', 'float')
    [1, 3, 3, 4.0]
    >>> pytypes_cdef(123)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    return c_pytypes_cdef(a, b, c, d)
