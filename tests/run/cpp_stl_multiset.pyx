# mode: run
# tag: cpp

# cython: language_level=3

from libcpp.set cimport multiset

def test_multiset_insert(vals):
    """
    >>> test_multiset_insert([1,2,2,3, -1])
    [-1, 1, 2, 2, 3]
    """
    cdef multiset[int] ms = multiset[int]()
    for v in vals:
        ms.insert(v)
    return [ item for item in ms ]

def test_multiset_count(vals, to_find):
    """
    >>> test_multiset_count([1,2,2,3, -1], 1)
    1
    >>> test_multiset_count([1,2,2,3, -1], 2)
    2
    """
    cdef multiset[int] ms = multiset[int]()
    for v in vals:
        ms.insert(v)
    return ms.count(to_find)

def test_multiset_erase(vals, int to_remove):
    """
    >>> test_multiset_erase([1,2,2,3, -1], 1)
    [-1, 2, 2, 3]
    >>> test_multiset_erase([1,2,2,3, -1], 2)  # removes both copies of 2
    [-1, 1, 3]
    """
    cdef multiset[int] ms = multiset[int]()
    for v in vals:
        ms.insert(v)
    ms.erase(to_remove)
    return [ item for item in ms ]

def test_multiset_finderase(vals, to_remove):
    """
    >>> test_multiset_finderase([1,2,2,3, -1], 1)
    [-1, 2, 2, 3]
    >>> test_multiset_finderase([1,2,2,3, -1], 2)  # removes a single copy of 2
    [-1, 1, 2, 3]
    """
    cdef multiset[int] ms = multiset[int]()
    for v in vals:
        ms.insert(v)
    it = ms.find(to_remove)
    ms.erase(it)
    return [ item for item in ms ]
