# mode: run
# tag: cpp, werror, cpp11, no-cpp-locals

from cython.operator cimport dereference as deref
from cython.operator cimport preincrement as incr

from libcpp.forward_list cimport forward_list
from libcpp cimport bool as cbool


def simple_iteration_test(L):
    """
    >>> iteration_test([1,2,4,8])
    8
    4
    2
    1
    >>> iteration_test([8,4,2,1])
    1
    2
    4
    8
    """
    cdef forward_list[int] l
    for a in L:
        l.push_front(a)
    for a in l:
        print(a)

def iteration_test(L):
    """
    >>> iteration_test([1,2,4,8])
    8
    4
    2
    1
    >>> iteration_test([8,4,2,1])
    1
    2
    4
    8
    """
    l = new forward_list[int]()
    try:
        for a in L:
            l.push_front(a)
        it = l.begin()
        while it != l.end():
            a = deref(it)
            incr(it)
            print(a)
    finally:
        del l

def test_value_type(x):
    """
    >>> test_value_type(2)
    2.0
    >>> test_value_type(2.5)
    2.5
    """
    cdef forward_list[double].value_type val = x
    return val

def test_value_type_complex(x):
    """
    >>> test_value_type_complex(2)
    (2+0j)
    """
    cdef forward_list[double complex].value_type val = x
    return val


#  Tests GitHub issue #1788.
cdef cppclass MyForwardList[T](forward_list):
    pass

cdef cppclass Ints(MyForwardList[int]):
    pass
