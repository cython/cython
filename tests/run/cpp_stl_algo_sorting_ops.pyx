# mode: run
# tag: cpp, werror, cpp11

from __future__ import print_function

from libcpp.algorithm cimport is_sorted, is_sorted_until
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
