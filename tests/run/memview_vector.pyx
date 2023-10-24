# mode: run
# tag: cpp

from libcpp.vector cimport vector

def memview_test(L, i32 i, i32 x):
    """
    >>> memview_test(range(10), 7, 100)
    [0, 1, 2, 3, 4, 5, 6, 100, 8, 9]
    """
    let vector[i32] v = L
    let i32[::1] mv = <i32[:len(L)]> &v[0]
    mv[i] = x
    return v
