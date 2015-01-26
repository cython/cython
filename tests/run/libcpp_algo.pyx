# tag: cpp

from libcpp cimport bool
from libcpp.algorithm cimport make_heap, sort_heap, sort, partial_sort
from libcpp.vector cimport vector


# XXX should use std::greater, but I don't know how to wrap that.
cdef inline bool greater(int x, int y):
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
        make_heap(v.begin(), v.end(), greater)
        sort_heap(v.begin(), v.end(), greater)
    else:
        make_heap(v.begin(), v.end())
        sort_heap(v.begin(), v.end())

    return v


def partialsort(l, int k, reverse=False):
    """
    >>> partialsort([4, 2, 3, 1, 5], k=2)[:2]
    [1, 2]
    >>> partialsort([4, 2, 3, 1, 5], k=2, reverse=True)[:2]
    [5, 4]
    """
    cdef vector[int] v = l
    if reverse:
        partial_sort(v.begin(), v.begin() + k, v.end(), greater)
    else:
        partial_sort(v.begin(), v.begin() + k, v.end())
    return v


def stdsort(l, reverse=False):
    """
    >>> stdsort([3, 2, 1, 4, 5])
    [1, 2, 3, 4, 5]
    >>> stdsort([3, 2, 1, 4, 5], reverse=True)
    [5, 4, 3, 2, 1]
    """
    cdef vector[int] v = l
    if reverse:
        sort(v.begin(), v.end(), greater)
    else:
        sort(v.begin(), v.end())
    return v
