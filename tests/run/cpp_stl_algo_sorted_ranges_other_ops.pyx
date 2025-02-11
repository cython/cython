# mode: run
# tag: cpp, werror, cpp11

from cython.operator cimport dereference as deref

from libcpp cimport bool
from libcpp.algorithm cimport merge, inplace_merge
from libcpp.vector cimport vector


cdef bool less(int a, int b):
    return a < b

def test_merge(vector[int] v1, vector[int] v2):
    """
    Test merge.

    >>> test_merge([1, 3, 5], [2, 4])
    [1, 2, 3, 4, 5]
    """
    cdef vector[int] out = vector[int](v1.size() + v2.size())
    merge(v1.begin(), v1.end(), v2.begin(), v2.end(), out.begin())
    return out

def test_merge_with_bin_pred(vector[int] v1, vector[int] v2):
    """
    Test merge with binary predicate

    >>> test_merge_with_bin_pred([1, 3, 5], [2, 4])
    [1, 2, 3, 4, 5]
    """
    cdef vector[int] out = vector[int](v1.size() + v2.size())
    merge(v1.begin(), v1.end(), v2.begin(), v2.end(), out.begin(), less)
    return out

def test_inplace_merge(vector[int] v):
    """
    Test inplace_merge.

    >>> test_inplace_merge([4, 5, 6, 1, 2, 3])
    [1, 2, 3, 4, 5, 6]
    """
    inplace_merge(v.begin(), v.begin() + 3, v.end())
    return v

def test_inplace_merge_with_bin_pred(vector[int] v):
    """
    Test inplace_merge with binary predicate

    >>> test_inplace_merge_with_bin_pred([4, 5, 6, 1, 2, 3])
    [1, 2, 3, 4, 5, 6]
    """
    inplace_merge(v.begin(), v.begin() + 3, v.end(), less)
    return v