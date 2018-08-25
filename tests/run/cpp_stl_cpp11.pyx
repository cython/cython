# mode: run
# tag: cpp, werror, cpp11

import sys
from libcpp.unordered_map cimport unordered_map
from libcpp.unordered_set cimport unordered_set
from libcpp.vector cimport vector
from libcpp.queue cimport queue
from libcpp.queue cimport priority_queue
from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.map cimport map
from libcpp.set cimport set
from libcpp.deque cimport deque


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


def test_queue_functionality():
    """
    >>> test_queue_functionality()
    'pass'
    """
    cdef:
        queue[int] int_queue = queue[int]()
        queue[int] int_queue2 = queue[int]()
    int_queue.push(77)
    int_queue.swap(int_queue2)
    assert int_queue.size() == 0
    assert int_queue2.size() == 1
    return "pass"


def test_deque_functionality():
    """
    >>> test_deque_functionality()
    'pass'
    """
    cdef:
        deque[int] int_deque = deque[int]()
    int_deque.push_back(77)
    int_deque.shrink_to_fit()
    return "pass"


def test_priority_queue_functionality():
    """
    >>> test_priority_queue_functionality()
    'pass'
    """
    cdef:
        priority_queue[int] int_queue = priority_queue[int]()
        priority_queue[int] int_queue2 = priority_queue[int]()
    int_queue.push(77)
    int_queue.swap(int_queue2)
    assert int_queue.size() == 0
    assert int_queue2.size() == 1
    return "pass"


def test_set_functionality():
    """
    >>> test_set_functionality()
    'pass'
    """
    cdef:
        set[int] int_set
        set[int] int_set2
    int_set2.insert(77)
    int_set2.insert(66)
    int_set.insert(int_set2.const_begin(), int_set2.const_end())
    assert int_set.size() == 2
    assert int_set.erase(int_set.const_begin(), int_set.const_end()) == int_set.end()
    return "pass"


def test_map_functionality():
    """
    >>> test_map_functionality()
    'pass'
    """
    cdef:
        map[int, const void*] int_map
        const void* data
    int_map[77] = NULL
    data = int_map.const_at(77)
    return "pass"


def test_unordered_set_functionality():
    """
    >>> test_unordered_set_functionality()
    'pass'
    """
    cdef:
        unordered_set[int] int_set = unordered_set[int]()
        unordered_set[int] int_set2
        unordered_set[int].iterator iterator = int_set.begin()
    int_set.insert(1)
    assert int_set.size() == 1
    int_set.erase(int_set.begin(), int_set.end())
    assert int_set.size() == 0
    int_set.insert(1)
    assert int_set.erase(1) == 1 # returns number of elements erased
    assert int_set.size() == 0
    int_set.insert(1)
    iterator = int_set.find(1)
    assert int_set.erase(iterator) == int_set.end()

    int_set2.insert(3)
    int_set2.insert(5)
    int_set.insert(int_set2.begin(), int_set2.end())
    assert int_set.size() == 2

    if sys.platform != 'darwin':
        int_set.max_load_factor(0.5)
        assert int_set.max_load_factor() == 0.5
    int_set.rehash(20)
    int_set.reserve(20)

    int_set.bucket_size(0)
    int_set.bucket_count()
    int_set.max_bucket_count()
    int_set.bucket(3)
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
        unordered_map[int, int] int_map2
        unordered_map[int, int*] intptr_map
        const int* intptr
    assert int_map[1] == 2
    assert int_map.size() == 1
    assert int_map.erase(1) == 1 # returns number of elements erased
    assert int_map.size() == 0
    int_map[1] = 2
    assert int_map.size() == 1
    assert int_map[1] == 2
    iterator = int_map.find(1)
    assert int_map.erase(iterator) == int_map.end()

    int_map2[1] = 2
    int_map2[3] = 3
    int_map.clear()
    int_map.insert(int_map2.begin(), int_map2.end())
    assert int_map.size() == 2
    assert int_map.erase(int_map.begin(), int_map.end()) == int_map.end()

    int_map.max_load_factor(0.5)
    assert int_map.max_load_factor() == 0.5
    int_map.rehash(20)
    int_map.reserve(20)

    int_map[3] = 3
    int_map.bucket_size(0)
    int_map.bucket_count()
    int_map.max_bucket_count()
    int_map.bucket(3)

    intptr_map[0] = NULL
    intptr = intptr_map.const_at(0)
    return "pass"
