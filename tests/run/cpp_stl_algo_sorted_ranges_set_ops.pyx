# mode: run
# tag: cpp, werror, cpp11

from libcpp cimport bool
from libcpp.algorithm cimport (includes, set_difference, set_intersection, 
                               set_symmetric_difference, set_union)
from libcpp.vector cimport vector


cdef bool less(int a, int b):
    return a < b

def test_includes(vector[int] v1, vector[int] v2):
    """
    Test includes.

    >>> test_includes([1, 2, 3, 4], [1, 2, 3])
    True
    >>> test_includes([1, 2, 3, 4], [5, 6, 7])
    False
    """
    return includes(v1.begin(), v1.end(), v2.begin(), v2.end())

def test_includes_with_bin_pred(vector[int] v1, vector[int] v2):
    """
    Test includes with binary predicate

    >>> test_includes_with_bin_pred([1, 2, 3, 4], [1, 2, 3])
    True
    >>> test_includes_with_bin_pred([1, 2, 3, 4], [5, 6, 7])
    False
    """
    return includes(v1.begin(), v1.end(), v2.begin(), v2.end(), less)

def test_set_difference(vector[int] v1, vector[int] v2):
    """
    Test set_difference.

    >>> test_set_difference([1, 2, 5, 5, 5, 9], [2, 5, 7])
    [1, 5, 5, 9]
    """
    cdef vector[int] diff = vector[int](4)
    set_difference(v1.begin(), v1.end(), v2.begin(), v2.end(), diff.begin())
    return diff

def test_set_difference_with_bin_pred(vector[int] v1, vector[int] v2):
    """
    Test set_difference with binary predicate

    >>> test_set_difference_with_bin_pred([1, 2, 5, 5, 5, 9], [2, 5, 7])
    [1, 5, 5, 9]
    """
    cdef vector[int] diff = vector[int](4)
    set_difference(v1.begin(), v1.end(), v2.begin(), v2.end(), diff.begin(), less)
    return diff

def test_set_intersection(vector[int] v1, vector[int] v2):
    """
    Test set_intersection.

    >>> test_set_intersection([1, 2, 3, 4, 5, 6, 7, 8], [5, 7, 9, 10])
    [5, 7]
    """
    cdef vector[int] out = vector[int](2)
    set_intersection(v1.begin(), v1.end(), v2.begin(), v2.end(), out.begin())
    return out

def test_set_intersection_with_bin_pred(vector[int] v1, vector[int] v2):
    """
    Test set_intersection with binary predicate

    >>> test_set_intersection_with_bin_pred([1, 2, 3, 4, 5, 6, 7, 8], [5, 7, 9, 10])
    [5, 7]
    """
    cdef vector[int] out = vector[int](2)
    set_intersection(v1.begin(), v1.end(), v2.begin(), v2.end(), out.begin(), less)
    return out

def test_set_symmetric_difference(vector[int] v1, vector[int] v2):
    """
    Test set_symmetric_difference.

    >>> test_set_symmetric_difference([1, 2, 3, 4, 5, 6, 7, 8], [5, 7, 9, 10])
    [1, 2, 3, 4, 6, 8, 9, 10]
    """
    cdef vector[int] out = vector[int](8)
    set_symmetric_difference(v1.begin(), v1.end(), v2.begin(), v2.end(), out.begin())
    return out

def test_set_symmetric_difference_with_bin_pred(vector[int] v1, vector[int] v2):
    """
    Test set_symmetric_difference with binary predicate

    >>> test_set_symmetric_difference_with_bin_pred([1, 2, 3, 4, 5, 6, 7, 8], [5, 7, 9, 10])
    [1, 2, 3, 4, 6, 8, 9, 10]
    """
    cdef vector[int] out = vector[int](8)
    set_symmetric_difference(v1.begin(), v1.end(), v2.begin(), v2.end(), out.begin(), less)
    return out

def test_set_union(vector[int] v1, vector[int] v2):
    """
    Test set_union.

    >>> test_set_union([1, 2, 3, 4, 5], [3, 4, 5, 6, 7])
    [1, 2, 3, 4, 5, 6, 7]
    """
    cdef vector[int] out = vector[int](7)
    set_union(v1.begin(), v1.end(), v2.begin(), v2.end(), out.begin())
    return out

def test_set_union_with_bin_pred(vector[int] v1, vector[int] v2):
    """
    Test set_union with binary predicate

    >>> test_set_union_with_bin_pred([1, 2, 3, 4, 5], [3, 4, 5, 6, 7])
    [1, 2, 3, 4, 5, 6, 7]
    """
    cdef vector[int] out = vector[int](7)
    set_union(v1.begin(), v1.end(), v2.begin(), v2.end(), out.begin(), less)
    return out