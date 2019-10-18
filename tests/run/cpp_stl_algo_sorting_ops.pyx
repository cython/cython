# mode: run
# tag: cpp, werror, cpp11

from __future__ import print_function

from libcpp.algorithm cimport is_sorted, is_sorted_until, sort, partial_sort
from libcpp.functional cimport greater
from libcpp.iterator cimport distance
from libcpp.vector cimport vector


def is_sorted_ints(vector[int] values):
    """
    Test is_sorted.

    >>> is_sorted_ints([3, 1, 4, 1, 5])
    False
    >>> is_sorted_ints([1, 1, 3, 4, 5])
    True
    """
    return is_sorted(values.begin(), values.end())


def initial_sorted_elements(vector[int] values):
    """
    Test is_sorted_until.

    >>> initial_sorted_elements([4, 1, 9, 5, 1, 3])
    1
    >>> initial_sorted_elements([4, 5, 9, 3, 1, 1])
    3
    >>> initial_sorted_elements([9, 3, 1, 4, 5, 1])
    1
    >>> initial_sorted_elements([1, 3, 5, 4, 1, 9])
    3
    >>> initial_sorted_elements([5, 9, 1, 1, 3, 4])
    2
    >>> initial_sorted_elements([4, 9, 1, 5, 1, 3])
    2
    >>> initial_sorted_elements([1, 1, 4, 9, 5, 3])
    4
    """
    sorted_end = is_sorted_until(values.begin(), values.end())
    return distance(values.begin(), sorted_end)


def sort_ints(vector[int] values):
    """Test sort using the default operator<.

    >>> sort_ints([5, 7, 4, 2, 8, 6, 1, 9, 0, 3])
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    sort(values.begin(), values.end())
    return values


def sort_ints_reverse(vector[int] values):
    """Test sort using a standard library comparison function object.

    >>> sort_ints_reverse([5, 7, 4, 2, 8, 6, 1, 9, 0, 3])
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    """
    sort(values.begin(), values.end(), greater[int]())
    return values


def partial_sort_ints(vector[int] values, int k):
    """
    Test partial_sort using the default operator<.

    >>> partial_sort_ints([4, 2, 3, 1, 5], 2)[:2]
    [1, 2]
    """
    partial_sort(values.begin(), values.begin() + k, values.end())
    return values


def partial_sort_ints_reverse(vector[int] values, int k):
    """
    Test partial_sort using a standard library comparison function object.

    >>> partial_sort_ints_reverse([4, 2, 3, 1, 5], 2)[:2]
    [5, 4]
    """
    partial_sort(values.begin(), values.begin() + k, values.end(), greater[int]())
    return values
