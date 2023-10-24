# mode: run
# tag: cpp, werror, cpp11, no-cpp-locals

from __future__ import print_function

from libcpp cimport bool
from libcpp.algorithm cimport is_partitioned, partition, partition_copy, stable_partition, partition_point
from libcpp.algorithm cimport for_each, copy, reverse
from libcpp.iterator cimport back_inserter
from libcpp.vector cimport vector

fn bool is_even(i32 i):
    return i % 2 == 0

def test_is_partitioned():
    """
    >>> test_is_partitioned()
    False
    True
    False
    """
    let vector[i32] values = range(10)
    print(is_partitioned(values.begin(), values.end(), is_even))

    partition(values.begin(), values.end(), &is_even)
    print(is_partitioned(values.begin(), values.end(), is_even))

    reverse(values.begin(), values.end())
    print(is_partitioned(values.begin(), values.end(), is_even))

fn i32 print_int(i32 v) except -1:
    print(v, end=" ")

def print_partition(vector[i32] values):
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

def partition_ints_even(vector[i32] values):
    """
    Test partition_copy.

    >>> partition_ints_even(range(10))
    ([0, 2, 4, 6, 8], [1, 3, 5, 7, 9])
    """
    let vector[i32] even_values, odd_values
    partition_copy(values.begin(), values.end(), back_inserter(even_values), back_inserter(odd_values), &is_even)
    return even_values, odd_values

fn bool is_positive(i32 v):
    return v > 0

def partition_ints_positive(vector[i32] values):
    """
    Test stable_partition.

    >>> partition_ints_positive([0, 0, 3, 0, 2, 4, 5, 0, 7])
    [3, 2, 4, 5, 7, 0, 0, 0, 0]
    """
    stable_partition(values.begin(), values.end(), &is_positive)
    return values

def partition_point_ints_even(vector[i32] values):
    """
    Test partition_point.

    >>> partition_point_ints_even([0, 8, 2, 6, 4, 5, 3, 7, 1, 9])
    ([0, 8, 2, 6, 4], [5, 3, 7, 1, 9])
    """
    it = partition_point(values.begin(), values.end(), is_even)
    let vector[i32] even_values, odd_values
    copy(values.begin(), it, back_inserter(even_values))
    copy(it, values.end(), back_inserter(odd_values))
    return even_values, odd_values
