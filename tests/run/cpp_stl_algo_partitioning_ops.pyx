# mode: run
# tag: cpp, werror, cpp11

from __future__ import print_function

from libcpp cimport bool
from libcpp.algorithm cimport is_partitioned, partition
from libcpp.algorithm cimport for_each, reverse
from libcpp.vector cimport vector


cdef bool is_even(int i):
    return i % 2 == 0


def test_is_partitioned():
    """
    >>> test_is_partitioned()
    False
    True
    False
    """
    cdef vector[int] values = range(10)
    print(is_partitioned(values.begin(), values.end(), is_even))

    partition(values.begin(), values.end(), &is_even)
    print(is_partitioned(values.begin(), values.end(), is_even))

    reverse(values.begin(), values.end())
    print(is_partitioned(values.begin(), values.end(), is_even))


cdef int print_int(int v) except -1:
    print(v, end=" ")


def print_partition(vector[int] values):
    """
    Test partition.

    >> print_partition(range(10))
    0 8 2 6 4  *  5 3 7 1 9
    """
    it = partition(values.begin(), values.end(), &is_even)
    for_each(values.begin(), it, &print_int)
    print("*", end=" ")
    for_each(it, values.end(), &print_int)
    print()
