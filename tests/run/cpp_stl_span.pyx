# mode: run
# tag: cpp, cpp20, no-cpp-locals, span

# cython: language_level=3

from cython.operator cimport dereference as deref
from cython.operator cimport preincrement as inc

from libcpp.span cimport dynamic_extent, span
from libcpp.utility cimport move
from libcpp.vector cimport vector

def test_span_construction_iterator_count(vals):
    """
    >>> test_span_construction_iterator_count([0, 1, 2, 3])
    [0, 1, 2, 3]
    """
    cdef vector[int] vec
    for v in vals:
        vec.push_back(v)
    cdef span[int] s = span[int](vec.data(), vec.size())
    return [val for val in s]

def test_span_construction_iterator_iterator(vals):
    """
    >>> test_span_construction_iterator_iterator([0, 1, 2, 3])
    [0, 1, 2, 3]
    """
    cdef vector[int] vec
    for v in vals:
        vec.push_back(v)
    cdef span[int] s = span[int](vec.data(), vec.data() + vec.size())
    return [val for val in s]

def test_span_construction_range(vals):
    """
    >>> test_span_construction_range([0, 1, 2, 3])
    [0, 1, 2, 3]
    """
    # construct the vector
    cdef vector[int] vec
    for v in vals:
        vec.push_back(v)
    cdef span[int] s = span[int](vec)
    return [val for val in s]

def test_span_data(vals):
    """
    >>> test_span_data([0, 1, 2, 3])
    True
    >>> test_span_data([1.25])
    True
    """
    cdef vector[double] vec
    for v in vals:
        vec.push_back(v)
    cdef span[double] s = span[double](vec.data(), vec.size())
    return vec.data() == s.data()

def test_span_empty(vals):
    """
    >>> test_span_empty([])
    True
    >>> test_span_empty([0, 1])
    False
    """
    cdef vector[double] vec
    for v in vals:
        vec.push_back(v)
    cdef span[double] s = span[double](vec.data(), vec.size())
    return s.empty()

def test_span_extent():
    """
    >>> test_span_extent()
    True
    """
    cdef span[int] s = span[int]()
    return s.extent == dynamic_extent

def test_span_first_last(vals, n):
    """
    >>> test_span_first_last([0, 1, 2, 3], 2)
    ([0, 1], [2, 3])
    >>> test_span_first_last([0, 1, 2, 3], 0)
    ([], [])
    """
    cdef vector[int] vec
    for v in vals:
        vec.push_back(v)
    cdef span[int] s = span[int](vec)
    return [val for val in s.first(n)], [val for val in s.last(n)]


def test_span_front_back(vals):
    """
    >>> test_span_front_back([0, 1, 2, 3])
    (0.0, 3.0)
    >>> test_span_front_back([1.25])
    (1.25, 1.25)
    """
    cdef vector[double] vec
    for v in vals:
        vec.push_back(v)
    cdef span[double] s = span[double](vec)
    return s.front(), s.back()

def test_span_index(vals):
    """
    >>> test_span_index([0, 1, 2, 3])
    (0.0, 3.0)
    >>> test_span_index([1.25])
    (1.25, 1.25)
    """
    cdef vector[double] vec
    for v in vals:
        vec.push_back(v)
    cdef span[double] s = span[double](vec)
    return s[0], s[s.size() - 1]

def test_span_reverse_iteration(vals):
    """
    >>> test_span_reverse_iteration([1, 2, 4, 8])
    8
    4
    2
    1
    """
    cdef vector[int] vec
    for v in vals:
        vec.push_back(v)
    cdef span[int] s = span[int](vec)

    it = s.rbegin()
    while it != s.rend():
        print(deref(it))
        inc(it)

def test_span_subspan(vals, offset):
    """
    >>> test_span_subspan([1, 2, 4, 8], 2)
    [4, 8]
    >>> test_span_subspan([1, 2, 4, 8], 1)
    [2, 4, 8]
    """
    cdef vector[int] vec
    for v in vals:
        vec.push_back(v)
    cdef span[int] s = span[int](vec)
    return [val for val in s.subspan(offset)]

def test_span_subspan_count(vals, offset, count):
    """
    >>> test_span_subspan_count([1, 2, 4, 8], 2, 1)
    [4]
    >>> test_span_subspan_count([1, 2, 4, 8], 1, 2)
    [2, 4]
    """
    cdef vector[int] vec
    for v in vals:
        vec.push_back(v)
    cdef span[int] s = span[int](vec)
    return [val for val in s.subspan(offset, count)]
