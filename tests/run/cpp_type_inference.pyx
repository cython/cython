# tag: cpp

from cython cimport typeof

from cython.operator cimport dereference as d
from cython.operator cimport preincrement as incr
from libcpp.vector cimport vector

def test_reversed_vector_iteration(L):
    """
    >>> test_reversed_vector_iteration([1,2,3])
    int: 3
    int: 2
    int: 1
    int
    """
    cdef vector[int] v = L

    it = v.rbegin()
    while it != v.rend():
        a = d(it)
        incr(it)
        print('%s: %s' % (typeof(a), a))
    print(typeof(a))
