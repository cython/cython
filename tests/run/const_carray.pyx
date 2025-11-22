# mode: run
# tag: const,carray

import cython


# Currently disallowed by SingleAssignmentNode:
'''
def const_carray():
    """
    >>> const_carray()
    [1, 2, 3]
    """
    cdef const int[3] array = [1, 2, 3]
    return array
'''


def const_carray_py():
    """
    >>> const_carray_py()
    [1, 2, 3]
    """
    array: cython.const[cython.int][3] = [1, 2, 3]
    return array


def carray_const_int():
    """
    >>> carray_const_int()
    [1, 2, 3]
    """
    cdef (const int)[3] array = [1, 2, 3]
    return array


def carray_const_int_py():
    """
    >>> carray_const_int_py()
    [1, 2, 3]
    """
    array: (cython.const[cython.int])[3] = [1, 2, 3]
    return array


# Currently disallowed by SingleAssignmentNode:
'''
def const_carray_int():
    """
    >>> const_carray_int()
    [1, 2, 3]
    """
    cdef const (int[3]) array = [1, 2, 3]
    return array


def const_carray_int_py():
    """
    >>> const_carray_int_py()
    [1, 2, 3]
    """
    array: cython.const[cython.int[3]] = [1, 2, 3]
    return array
'''
