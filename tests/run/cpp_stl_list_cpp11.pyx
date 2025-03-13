# mode: run
# tag: cpp, werror, no-cpp-locals, cpp11

from cython.operator cimport dereference as deref
from cython.operator cimport preincrement as incr

from libcpp.list cimport list as cpp_list

def const_iteration_test(L):
    """
    >>> const_iteration_test([1,2,4,8])
    1
    2
    4
    8
    """
    l = new cpp_list[int]()
    try:
        for a in L:
            l.push_back(a)
        it = l.cbegin()
        while it != l.cend():
            a = deref(it)
            incr(it)
            print(a)
    finally:
        del l

cdef list const_to_pylist(cpp_list[int]& l):
    cdef list L = []
    it = l.cbegin()
    while it != l.cend():
        L.append(deref(it))
        incr(it)
    return L

def const_item_ptr_test(L, int x):
    """
    >>> const_item_ptr_test(range(10), 100)
    [100, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    cdef cpp_list[int] l = L
    cdef int* li_ptr = &l.front()
    li_ptr[0] = x
    return const_to_pylist(l)
