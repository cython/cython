# mode: run
# tag: cpp, werror, no-cpp-locals

from cython.operator cimport dereference as deref
from cython.operator cimport preincrement as incr

from libcpp.list cimport list as cpp_list
from libcpp cimport bool as cbool


def simple_test(double x):
    """
    >>> simple_test(55)
    3
    """
    l = new cpp_list[double]()
    try:
        l.push_back(1.0)
        l.push_back(x)
        from math import pi
        l.push_back(pi)
        return l.size()
    finally:
        del l

def pylist_test(L):
    """
    >>> pylist_test([1,2,4,8])
    (4, 4)
    >>> pylist_test([])
    (0, 0)
    >>> pylist_test([-1] * 1000)
    (1000, 1000)
    """
    l = new cpp_list[int]()
    try:
        for a in L:
            l.push_back(a)
        return len(L), l.size()
    finally:
        del l


def iteration_test(L):
    """
    >>> iteration_test([1,2,4,8])
    1
    2
    4
    8
    """
    l = new cpp_list[int]()
    try:
        for a in L:
            l.push_back(a)
        it = l.begin()
        while it != l.end():
            a = deref(it)
            incr(it)
            print(a)
    finally:
        del l

def reverse_iteration_test(L):
    """
    >>> reverse_iteration_test([1,2,4,8])
    8
    4
    2
    1
    """
    l = new cpp_list[int]()
    try:
        for a in L:
            l.push_back(a)
        it = l.rbegin()
        while it != l.rend():
            a = deref(it)
            incr(it)
            print(a)
    finally:
        del l

def nogil_test(L):
    """
    >>> nogil_test([1,2,3])
    3
    """
    cdef int a
    with nogil:
        l = new cpp_list[int]()
    try:
        for a in L:
            with nogil:
                l.push_back(a)
        return l.size()
    finally:
        del l


cdef list to_pylist(cpp_list[int]& l):
    cdef list L = []
    it = l.begin()
    while it != l.end():
        L.append(deref(it))
        incr(it)
    return L

def item_ptr_test(L, int x):
    """
    >>> item_ptr_test(range(10), 100)
    [100, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    cdef cpp_list[int] l = L
    cdef int* li_ptr = &l.front()
    li_ptr[0] = x
    return to_pylist(l)

def test_value_type(x):
    """
    >>> test_value_type(2)
    2.0
    >>> test_value_type(2.5)
    2.5
    """
    cdef cpp_list[double].value_type val = x
    return val

def test_value_type_complex(x):
    """
    >>> test_value_type_complex(2)
    (2+0j)
    """
    cdef cpp_list[double complex].value_type val = x
    return val

def test_insert():
    """
    >>> test_insert()
    """
    cdef cpp_list[int] l
    cdef cpp_list[int].size_type count = 5
    cdef int value = 0

    l.insert(l.end(), count, value)

    assert l.size() == count
    for element in l:
        assert element == value, '%s != %s' % (element, count)


#  Tests GitHub issue #1788.
cdef cppclass MyList[T](cpp_list):
    pass

cdef cppclass Ints(MyList[int]):
    pass
