# mode: run
# tag: cpp, werror, cpp17, no-cpp-locals, c_string_type=str
# cython: c_string_encoding=ascii, c_string_type=str

from libcpp cimport bool
from libcpp.algorithm cimport is_permutation, next_permutation, prev_permutation
from libcpp.vector cimport vector
from libcpp.string cimport string

cdef bool compare(int a, int b):
    return a == b

cdef bool less_than(char a, char b):
    return a < b

def test_is_permutation(vector[int] v1, vector[int] v2):
    """
    Test is_permutation.

    >>> test_is_permutation([1, 2, 3, 4], [4, 2, 3, 1])
    True
    >>> test_is_permutation([1, 2, 3, 4], [4, 4, 2, 5])
    False
    """
    return is_permutation(v1.begin(), v1.end(), v2.begin())

def test_is_permutation_with_bin_pred(vector[int] v1, vector[int] v2):
    """
    Test is_permutation with binary predicate

    >>> test_is_permutation_with_bin_pred([1, 2, 3, 4], [4, 2, 3, 1])
    True
    >>> test_is_permutation_with_bin_pred([1, 2, 3, 4], [4, 4, 2, 5])
    False
    """
    return is_permutation(v1.begin(), v1.end(), v2.begin(), compare)

def test_is_permutation_with_second_range_and_bin_pred(vector[int] v1, vector[int] v2):
    """
    Test is_permutation with second range and binary predicate

    >>> test_is_permutation_with_second_range_and_bin_pred([1, 2, 3, 4], [4, 2, 3, 1])
    True
    >>> test_is_permutation_with_second_range_and_bin_pred([1, 2, 3, 4], [4, 4, 2, 5])
    False
    """
    return is_permutation(v1.begin(), v1.end(), v2.begin(), v2.end(), compare)

def test_next_permutation(s_in, s_perm):
    """
    Test next_permutation.

    >>> test_next_permutation("aba", "baa")
    True
    >>> test_next_permutation("aba", "bab")
    False
    """
    cdef string ss = <char*>s_in
    cdef string expected = <char*>s_perm
    next_permutation(ss.begin(), ss.end())
    return ss == expected

def test_next_permutation_with_bin_pred(s_in, s_perm):
    """
    Test next_permutation with binary predicate

    >>> test_next_permutation_with_bin_pred("aba", "baa")
    True
    >>> test_next_permutation_with_bin_pred("aba", "bab")
    False
    """
    cdef string ss = <char*>s_in
    cdef string expected = <char*>s_perm
    next_permutation(ss.begin(), ss.end(), less_than)
    return ss == expected

def test_prev_permutation(s_in, s_perm):
    """
    Test prev_permutation.

    >>> test_prev_permutation("aba", "aab")
    True
    >>> test_prev_permutation("aba", "bab")
    False
    """
    cdef string ss = <char*>s_in
    cdef string expected = <char*>s_perm
    prev_permutation(ss.begin(), ss.end())
    return ss == expected

def test_prev_permutation_with_bin_pred(s_in, s_perm):
    """
    Test prev_permutation with binary predicate

    >>> test_prev_permutation_with_bin_pred("aba", "aab")
    True
    >>> test_prev_permutation_with_bin_pred("aba", "bab")
    False
    """
    cdef string ss = <char*>s_in
    cdef string expected = <char*>s_perm
    prev_permutation(ss.begin(), ss.end(), less_than)
    return ss == expected
