# mode: run
# tag: cpp, werror, cpp17, cppexecpolicies

from cython.operator cimport dereference as deref

from libcpp cimport bool
from libcpp.algorithm cimport (min_element, max_element, minmax, minmax_element, 
                               clamp)
from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.execution cimport seq


cdef bool less(int a, int b):
    return a < b

def test_min_element(vector[int] v):
    """
    Test min_element.

    >>> test_min_element([0, 1, 2, 3, 4, 5])
    0
    """
    cdef vector[int].iterator it = min_element(v.begin(), v.end())
    return deref(it)

def test_min_element_with_pred(vector[int] v):
    """
    Test min_element with binary predicate.

    >>> test_min_element_with_pred([0, 1, 2, 3, 4, 5])
    0
    """
    cdef vector[int].iterator it = min_element(v.begin(), v.end(), less)
    return deref(it)

def test_min_element_with_exec(vector[int] v):
    """
    Test min_element with execution policy.

    >>> test_min_element_with_exec([0, 1, 2, 3, 4, 5])
    0
    """
    cdef vector[int].iterator it = min_element(seq, v.begin(), v.end())
    return deref(it)

def test_max_element(vector[int] v):
    """
    Test max_element.

    >>> test_max_element([0, 1, 2, 3, 4, 5])
    5
    """
    cdef vector[int].iterator it = max_element(v.begin(), v.end())
    return deref(it)

def test_max_element_with_pred(vector[int] v):
    """
    Test max_element with binary predicate.

    >>> test_max_element_with_pred([0, 1, 2, 3, 4, 5])
    5
    """
    cdef vector[int].iterator it = max_element(v.begin(), v.end(), less)
    return deref(it)

def test_max_element_with_exec(vector[int] v):
    """
    Test max_element with execution policy.

    >>> test_max_element_with_exec([0, 1, 2, 3, 4, 5])
    5
    """
    cdef vector[int].iterator it = max_element(seq, v.begin(), v.end())
    return deref(it)

def test_minmax(int a, int b):
    """
    Test minmax.

    >>> test_minmax(10, 20)
    [10, 20]
    """
    cdef pair[int, int] p = minmax(a, b)
    return [p.first, p.second]

def test_minmax_with_pred(int a, int b):
    """
    Test minmax with binary predicate.

    >>> test_minmax_with_pred(10, 20)
    [10, 20]
    """
    cdef pair[int, int] p = minmax(a, b, less)
    return [p.first, p.second]

def test_minmax_element(vector[int] v):
    """
    Test minmax_element.

    >>> test_minmax_element([0, 1, 2, 3, 4, 5])
    [0, 5]
    """
    cdef pair[vector[int].iterator, vector[int].iterator] p = minmax_element(v.begin(), v.end())
    return [deref(p.first), deref(p.second)]

def test_minmax_element_with_pred(vector[int] v):
    """
    Test minmax_element with binary predicate.

    >>> test_minmax_element_with_pred([0, 1, 2, 3, 4, 5])
    [0, 5]
    """
    cdef pair[vector[int].iterator, vector[int].iterator] p = minmax_element(v.begin(), v.end(), less)
    return [deref(p.first), deref(p.second)]

def test_minmax_element_with_exec(vector[int] v):
    """
    Test minmax_element with execution policy.

    >>> test_minmax_element_with_exec([0, 1, 2, 3, 4, 5])
    [0, 5]
    """
    cdef pair[vector[int].iterator, vector[int].iterator] p = minmax_element(seq, v.begin(), v.end())
    return [deref(p.first), deref(p.second)]

def test_clamp(int v, int lo, int hi):
    """
    Test clamp.

    >>> test_clamp(-129, -128, 255)
    -128
    """
    return clamp(v, lo, hi)

def test_clamp_with_pred(int v, int lo, int hi):
    """
    Test clamp with binary predicate

    >>> test_clamp_with_pred(-129, -128, 255)
    -128
    """
    return clamp(v, lo, hi, less)