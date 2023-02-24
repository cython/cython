# mode: run
# tag: cpp, cpp20

# cython: language_level=3

from libcpp.map cimport map, multimap
from libcpp.set cimport set, multiset
from libcpp.unordered_map cimport unordered_map, unordered_multimap
from libcpp.unordered_set cimport unordered_set, unordered_multiset

def test_map_contains(vals, int key_to_find):
    """
    >>> test_map_contains([(1,100),(2,200),(3,300)], 3)
    True
    >>> test_map_contains([(1,100),(2,200),(3,300)], 4)
    False
    """
    cdef map[int,int] m = map[int, int]()
    for v in vals:
        m.insert(v)
    return m.contains(key_to_find)

def test_unordered_map_contains(vals, int key_to_find):
    """
    >>> test_unordered_map_contains([(1,100),(2,200),(3,300)], 3)
    True
    >>> test_unordered_map_contains([(1,100),(2,200),(3,300)], 4)
    False
    """
    cdef unordered_map[int,int] um = unordered_map[int, int]()
    for v in vals:
        um.insert(v)
    return um.contains(key_to_find)

def test_multimap_contains(vals, int key_to_find):
    """
    >>> test_multimap_contains([(1,100),(2,200),(3,300)], 3)
    True
    >>> test_multimap_contains([(1,100),(2,200),(3,300)], 4)
    False
    """
    cdef multimap[int,int] mm = multimap[int, int]()
    for v in vals:
        mm.insert(v)
    return mm.contains(key_to_find)

def test_unordered_multimap_contains(vals, int key_to_find):
    """
    >>> test_unordered_multimap_contains([(1,100),(2,200),(3,300)], 3)
    True
    >>> test_unordered_multimap_contains([(1,100),(2,200),(3,300)], 4)
    False
    """
    cdef unordered_multimap[int,int] umm = unordered_multimap[int, int]()
    for v in vals:
        umm.insert(v)
    return umm.contains(key_to_find)


def test_set_contains(vals, int val_to_find):
    """
    >>> test_set_contains([1, 2, 3], 3)
    True
    >>> test_set_contains([1, 2, 3], 4)
    False
    """
    cdef set[int] s = set[int]()
    for v in vals:
        s.insert(v)
    return s.contains(val_to_find)

def test_unordered_set_contains(vals, int val_to_find):
    """
    >>> test_unordered_set_contains([1, 2, 3], 3)
    True
    >>> test_unordered_set_contains([1, 2, 3], 4)
    False
    """
    cdef unordered_set[int] us = unordered_set[int]()
    for v in vals:
        us.insert(v)
    return us.contains(val_to_find)

def test_multiset_contains(vals, int val_to_find):
    """
    >>> test_multiset_contains([1, 2, 3], 3)
    True
    >>> test_multiset_contains([1, 2, 3], 4)
    False
    """
    cdef multiset[int] ms = multiset[int]()
    for v in vals:
        ms.insert(v)
    return ms.contains(val_to_find)

def test_unordered_multiset_contains(vals, int val_to_find):
    """
    >>> test_unordered_multiset_contains([1, 2, 3], 3)
    True
    >>> test_unordered_multiset_contains([1, 2, 3], 4)
    False
    """
    cdef unordered_multiset[int] ums = unordered_multiset[int]()
    for v in vals:
        ums.insert(v)
    return ums.contains(val_to_find)
