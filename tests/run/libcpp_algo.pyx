# mode: run
# tag: cpp

from libcpp cimport bool
from libcpp.algorithm cimport make_heap, sort_heap
from libcpp.vector cimport vector


# XXX should use std::greater, but I don't know how to wrap that.
cdef inline bool greater(const int &x, const int &y):
    return x > y


def heapsort(l, bool reverse=False):
    """
    >>> heapsort([3, 5, 1, 0, 2, 4])
    [0, 1, 2, 3, 4, 5]
    >>> heapsort([3, 5, 1, 0, 2, 4], reverse=True)
    [5, 4, 3, 2, 1, 0]
    """
    cdef vector[int] v = l

    if reverse:
        make_heap(v.begin(), v.end(), &greater)
        sort_heap(v.begin(), v.end(), &greater)
    else:
        make_heap(v.begin(), v.end())
        sort_heap(v.begin(), v.end())

    return v
