# mode: run
# tag: cpp

from libcpp.vector cimport vector

def memview_test(L, int i, int x):
    """
    >>> memview_test(range(10), 7, 100)
    [0, 1, 2, 3, 4, 5, 6, 100, 8, 9]
    """
    cdef vector[int] v = L
    cdef int[::1] mv = <int[:len(L)]> &v[0]
    mv[i] = x
    return v
