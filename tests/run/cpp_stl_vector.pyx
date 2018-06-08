# mode: run
# tag: cpp, werror

from cython.operator cimport dereference as d
from cython.operator cimport preincrement as incr

from libcpp.vector cimport vector
from libcpp cimport bool as cbool

def simple_test(double x):
    """
    >>> simple_test(55)
    3
    """
    v = new vector[double]()
    try:
        v.push_back(1.0)
        v.push_back(x)
        from math import pi
        v.push_back(pi)
        return v.size()
    finally:
        del v

def list_test(L):
    """
    >>> list_test([1,2,4,8])
    (4, 4)
    >>> list_test([])
    (0, 0)
    >>> list_test([-1] * 1000)
    (1000, 1000)
    """
    v = new vector[int]()
    try:
        for a in L:
            v.push_back(a)
        return len(L), v.size()
    finally:
        del v

def index_test(L):
    """
    >>> index_test([1,2,4,8])
    (1.0, 8.0)
    >>> index_test([1.25])
    (1.25, 1.25)
    """
    v = new vector[double]()
    try:
        for a in L:
            v.push_back(a)
        return v[0][0], v[0][len(L)-1]
    finally:
        del v


def index_set_test(L):
    """
    >>> index_set_test([1,2,4,8])
    (-1.0, -8.0)
    >>> index_set_test([1.25])
    (-1.25, -1.25)
    """
    v = new vector[double]()
    try:
        for a in L:
            v.push_back(a)
        for i in range(v.size()):
            d(v)[i] = -d(v)[i]
        return d(v)[0], d(v)[v.size()-1]
    finally:
        del v

def iteration_test(L):
    """
    >>> iteration_test([1,2,4,8])
    1
    2
    4
    8
    """
    v = new vector[int]()
    try:
        for a in L:
            v.push_back(a)
        it = v.begin()
        while it != v.end():
            a = d(it)
            incr(it)
            print(a)
    finally:
        del v

def reverse_iteration_test(L):
    """
    >>> reverse_iteration_test([1,2,4,8])
    8
    4
    2
    1
    """
    v = new vector[int]()
    try:
        for a in L:
            v.push_back(a)
        it = v.rbegin()
        while it != v.rend():
            a = d(it)
            incr(it)
            print(a)
    finally:
        del v

def nogil_test(L):
    """
    >>> nogil_test([1,2,3])
    3
    """
    cdef int a
    with nogil:
        v = new vector[int]()
    try:
        for a in L:
            with nogil:
                v.push_back(a)
        return v.size()
    finally:
        del v

def item_ptr_test(L, int i, int x):
    """
    >>> item_ptr_test(range(10), 7, 100)
    [0, 1, 2, 3, 4, 5, 6, 100, 8, 9]
    """
    cdef vector[int] v = L
    cdef int* vi_ptr = &v[i]
    vi_ptr[0] = x
    return v

def test_value_type(x):
    """
    >>> test_value_type(2)
    2.0
    >>> test_value_type(2.5)
    2.5
    """
    cdef vector[double].value_type val = x
    return val

def test_value_type_complex(x):
    """
    >>> test_value_type_complex(2)
    (2+0j)
    """
    cdef vector[double complex].value_type val = x
    return val

def test_bool_vector_convert(o):
    """
    >>> test_bool_vector_convert([True, False, None, 3])
    [True, False, False, True]
    """
    cdef vector[cbool] v = o
    return v

def test_bool_vector_get_set():
    """
    >>> test_bool_vector_get_set()
    """
    cdef vector[cbool] v = range(5)
    # Test access.
    assert not v[0], v
    assert v[1], v
    assert not v.at(0), v
    assert v.at(1), v
    v[0] = True
    v[1] = False
    assert <object>v == [True, False, True, True, True]

ctypedef vector[cbool] vector_bool
ctypedef vector[int] vector_int

def test_typedef_vector(L):
    """
    >>> test_typedef_vector([0, 1, True])
    ([0, 1, 1, 0, 1, 1], 0, [False, True, True, False, True, True], False)
    """
    cdef vector_int vi = L
    cdef vector_int vi2 = vi
    vi.insert(vi.begin(), vi2.begin(), vi2.end())

    cdef vector_bool vb = L
    cdef vector_bool vb2 = vb
    vb.insert(vb.begin(), vb2.begin(), vb2.end())

    return vi, vi.at(0), vb, vb.at(0)


def test_insert():
    """
    >>> test_insert()
    """
    cdef vector[int] v
    cdef vector[int].size_type count = 5
    cdef int value = 0

    v.insert(v.end(), count, value)

    assert v.size() == count
    for element in v:
        assert element == value, '%s != %s' % (element, count)


#  Tests GitHub issue #1788.
cdef cppclass MyVector[T](vector):
    pass

cdef cppclass Ints(MyVector[int]):
    pass
