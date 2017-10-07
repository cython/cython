# mode: run
# tag: cpp, werror, cpp11
# distutils: extra_compile_args=-std=c++0x

import sys
from libcpp.unordered_map cimport unordered_map
from libcpp.pair cimport pair

py_set = set
py_xrange = xrange
py_unicode = unicode



def test_unordered_map_functionality():
    """
        tests basic unordered map functionality
        checks insertion with Pair and [] operator
        checks erase with pair and and key
        
    """
    cdef:
        unordered_map[int, int] int_map = unordered_map[int,int]()
        pair[int, int] pair_insert = pair[int, int](1, 2)
        unordered_map[int,int].iterator iterator = int_map.begin()
        pair[unordered_map[int,int].iterator, bint] pair_iter  = int_map.insert(pair_insert)
    assert int_map[1] == 2
    assert int_map.size() == 1
    assert int_map.erase(pair_insert) == int_map.end()
    assert int_map.size() == 0
    int_map[1] = 2
    assert int_map.size() == 1
    assert int_map[1] == 2
    assert int_map.erase(1) == int_map.end()


