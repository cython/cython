# mode: run
# tag: cpp, cpp11

# cython: language_level=3

from libcpp.map cimport map
from libcpp.unordered_map cimport unordered_map
from libcpp.utility cimport pair

def test_map_insert(vals):
    """
    >>> test_map_insert([(1,1),(2,2),(2,2),(3,3),(-1,-1)])
    [(-1, -1), (1, 1), (2, 2), (3, 3)]
    """
    cdef map[int,int] m = map[int, int]()
    cdef pair[map[int, int].iterator, bint] ret
    for v in vals:
        ret = m.insert(v)
    return [ (item.first, item.second) for item in m ]

def test_map_insert_it(vals):
    """
    >>> test_map_insert_it([(1,1),(2,2),(2,2),(3,3),(-1,-1)])
    [(-1, -1), (1, 1), (2, 2), (3, 3)]
    """
    cdef unordered_map[int,int] um = unordered_map[int,int]()
    cdef map[int,int] m = map[int,int]()
    for k, v in vals:
        um.insert(pair[int,int](k, v))
    m.insert(um.begin(), um.end())
    return [ (item.first, item.second) for item in m ]

def test_const_map_insert_it(vals):
    """
    >>> test_const_map_insert_it([(1,1),(2,2),(2,2),(3,3),(-1,-1)])
    [(-1, -1), (1, 1), (2, 2), (3, 3)]
    """
    cdef unordered_map[int,int] um = unordered_map[int,int]()
    cdef map[int,int] m = map[int,int]()
    for k, v in vals:
        um.insert(pair[int,int](k, v))
    m.insert(um.cbegin(), um.cend())
    return [ (item.first, item.second) for item in m ]

def test_map_count(vals, to_find):
    """
    >>> test_map_count([(1,1),(2,2),(2,2),(3,3),(-1,-1)], 1)
    1
    >>> test_map_count([(1,1),(2,2),(2,2),(3,3),(-1,-1)], 2)
    1
    """
    cdef map[int,int] m = map[int,int]()
    for v in vals:
        m.insert(v)
    return m.count(to_find)

def test_map_erase(vals, int to_remove):
    """
    >>> test_map_erase([(1,1),(2,2),(2,2),(3,3),(-1,-1)], 1)
    [(-1, -1), (2, 2), (3, 3)]
    >>> test_map_erase([(1,1),(2,2),(2,2),(3,3),(-1,-1)], 2)
    [(-1, -1), (1, 1), (3, 3)]
    """
    cdef map[int,int] m = map[int,int]()
    cdef size_t ret
    for v in vals:
        m.insert(v)
    ret = m.erase(to_remove)
    return [ (item.first, item.second) for item in m ]

def test_map_find_erase(vals, to_remove):
    """
    >>> test_map_find_erase([(1,1),(2,2),(2,2),(3,3),(-1,-1)], 1)
    [(-1, -1), (2, 2), (3, 3)]
    >>> test_map_find_erase([(1,1),(2,2),(2,2),(3,3),(-1,-1)], 2)
    [(-1, -1), (1, 1), (3, 3)]
    """
    cdef map[int,int] m = map[int,int]()
    cdef map[int,int].iterator it
    for v in vals:
        m.insert(v)
    it = m.find(to_remove)
    it = m.erase(it)
    return [ (item.first, item.second) for item in m ]


def test_unordered_map_insert(vals):
    """
    >>> test_unordered_map_insert([(1,1),(2,2),(2,2),(3,3),(-1,-1)])
    [(-1, -1), (1, 1), (2, 2), (3, 3)]
    """
    cdef unordered_map[int,int] um = unordered_map[int,int]()
    cdef pair[unordered_map[int,int].iterator, bint] ret
    for v in vals:
        ret = um.insert(v)
    return sorted([ (item.first, item.second) for item in um ])

def test_unordered_map_insert_it(vals):
    """
    >>> test_unordered_map_insert_it([(1,1),(2,2),(2,2),(3,3),(-1,-1)])
    [(-1, -1), (1, 1), (2, 2), (3, 3)]
    """
    cdef map[int,int] m = map[int,int]()
    cdef unordered_map[int,int] um = unordered_map[int,int]()
    for v in vals:
        m.insert(v)
    um.insert(m.begin(), m.end())
    return sorted([ (item.first, item.second) for item in um ])

def test_const_unordered_map_insert_it(vals):
    """
    >>> test_const_unordered_map_insert_it([(1,1),(2,2),(2,2),(3,3),(-1,-1)])
    [(-1, -1), (1, 1), (2, 2), (3, 3)]
    """
    cdef map[int,int] m = map[int,int]()
    cdef unordered_map[int,int] um = unordered_map[int,int]()
    for v in vals:
        m.insert(v)
    um.insert(m.cbegin(), m.cend())
    return sorted([ (item.first, item.second) for item in um ])

def test_unordered_map_count(vals, to_find):
    """
    >>> test_unordered_map_count([(1,1),(2,2),(2,2),(3,3),(-1,-1)], 1)
    1
    >>> test_unordered_map_count([(1,1),(2,2),(2,2),(3,3),(-1,-1)], 2)
    1
    """
    cdef unordered_map[int,int] um = unordered_map[int,int]()
    for v in vals:
        um.insert(v)
    return um.count(to_find)

def test_unordered_map_erase(vals, int to_remove):
    """
    >>> test_unordered_map_erase([(1,1),(2,2),(2,2),(3,3),(-1,-1)], 1)
    [(-1, -1), (2, 2), (3, 3)]
    >>> test_unordered_map_erase([(1,1),(2,2),(2,2),(3,3),(-1,-1)], 2)
    [(-1, -1), (1, 1), (3, 3)]
    """
    cdef unordered_map[int,int] um = unordered_map[int,int]()
    cdef size_t ret
    for v in vals:
        um.insert(v)
    ret = um.erase(to_remove)
    return sorted([ (item.first, item.second) for item in um ])

def test_unordered_map_find_erase(vals, to_remove):
    """
    >>> test_unordered_map_find_erase([(1,1),(2,2),(2,2),(3,3),(-1,-1)], 1)
    [(-1, -1), (2, 2), (3, 3)]
    >>> test_unordered_map_find_erase([(1,1),(2,2),(2,2),(3,3),(-1,-1)], 2)
    [(-1, -1), (1, 1), (3, 3)]
    """
    cdef unordered_map[int,int] um = unordered_map[int,int]()
    cdef unordered_map[int,int].iterator it
    for v in vals:
        um.insert(v)
    it = um.find(to_remove)
    it = um.erase(it)
    return sorted([ item for item in um ])

def test_iterator_stack_allocated():
    """
    https://github.com/cython/cython/issues/4657 - mainly a compile test showing
    that const iterators can be stack allocated
    >>> test_iterator_stack_allocated()
    """
    cdef map[int,int] mymap = map[int,int]()
    cdef unordered_map[int,int] myumap = unordered_map[int,int]()
    cdef int ckey = 5
    it = mymap.const_find(ckey)
    assert it == mymap.const_end()
    uit = myumap.const_find(ckey)
    assert uit == myumap.const_end()
