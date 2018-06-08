cimport cython.operator
from cython.operator cimport dereference
from cython.operator cimport dereference as deref

def test_deref(int x):
    """
    >>> test_deref(3)
    (3, 3, 3)
    >>> test_deref(5)
    (5, 5, 5)
    """
    cdef int* x_ptr = &x
    return cython.operator.dereference(x_ptr), dereference(x_ptr), deref(x_ptr)

def increment_decrement(int x):
    """
    >>> increment_decrement(10)
    11 11 12
    11 11 10
    10
    """
    print cython.operator.preincrement(x), cython.operator.postincrement(x), x
    print cython.operator.predecrement(x), cython.operator.postdecrement(x), x
    return x
