cimport cython

def test_deref(int x):
    """
    >>> test_deref(3)
    3
    >>> test_deref(5)
    5
    """
    cdef int* x_ptr = &x
    return cython.dereference(x_ptr)

def increment_decrement(int x):
    """
    >>> increment_decrement(10)
    11 11 12
    11 11 10
    10
    """
    print cython.preincrement(x), cython.postincrement(x), x
    print cython.predecrement(x), cython.postdecrement(x), x
    return x
