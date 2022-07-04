# mode: run
# tag: cpp, werror, no-cpp-locals, cpp11

from cython.operator cimport dereference as d
from cython.operator cimport preincrement as incr

from libcpp.vector cimport vector

def const_iteration_test(L):
    """
    >>> const_iteration_test([1,2,4,8])
    1
    2
    4
    8
    """
    v = new vector[int]()
    try:
        for a in L:
            v.push_back(a)
        it = v.cbegin()
        while it != v.cend():
            a = d(it)
            incr(it)
            print(a)
    finally:
        del v
