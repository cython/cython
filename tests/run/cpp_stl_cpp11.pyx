# mode: run
# tag: cpp, werror, cpp11
# distutils: extra_compile_args=-std=c++0x

import sys
from libcpp.unordered_map cimport unordered_map
from libcpp.vector cimport vector
from libcpp.vector cimport vector
from libcpp.pair cimport pair


def test_vector_functionality():
    """
    >>> test_vector_functionality()
    'pass'
    """
    cdef:
        vector[int] int_vector = vector[int]()
        int* data
        const int* const_data
    int_vector.push_back(77)
    data = int_vector.data()
    const_data = int_vector.const_data()
    assert data[0] == 77
    assert const_data[0] == 77
    return "pass"


def test_unordered_map_functionality():
    """
    >>> test_unordered_map_functionality()
    'pass'
    """
    cdef:
        unordered_map[int, int] int_map = unordered_map[int,int]()
        pair[int, int] pair_insert = pair[int, int](1, 2)
        unordered_map[int,int].iterator iterator = int_map.begin()
        pair[unordered_map[int,int].iterator, bint] pair_iter  = int_map.insert(pair_insert)
    assert int_map[1] == 2
    assert int_map.size() == 1
    assert int_map.erase(1) == 1 # returns number of elements erased
    assert int_map.size() == 0
    int_map[1] = 2
    assert int_map.size() == 1
    assert int_map[1] == 2
    iterator = int_map.find(1)
    assert int_map.erase(iterator) == int_map.end()
    return "pass"


