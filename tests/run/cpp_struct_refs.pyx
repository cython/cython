# mode: run
# tag: cpp

from libcpp.vector cimport vector

cdef struct S:
    int number

def construct_and_push_back(int number):
    """
    >>> construct_and_push_back(5)
    5
    """
    v = vector[S]()
    # The struct should be constructed with a type of S,
    # rather than a type of const S&
    v.push_back(S(number))
    return v.back().number
