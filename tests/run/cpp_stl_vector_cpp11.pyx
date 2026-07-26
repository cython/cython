# mode: run
# tag: cpp, werror, no-cpp-locals, cpp11

from cython.operator cimport dereference as d
from cython.operator cimport preincrement as incr

from libcpp.vector cimport vector

ctypedef vector[int] ivector

def test_vector_data():
    """
    >>> test_vector_data()
    (77, 77)
    """
    cdef:
        int* data
        const int* const_data
    int_vector = ivector()
    int_vector.push_back(77)
    data = int_vector.data()
    const_data = int_vector.const_data()
    return data[0], const_data[0]

def test_vector_emplace():
    """
    >>> test_vector_emplace()
    [0, 7]
    """
    cdef ivector v
    v.emplace(v.cend())
    v.emplace(v.cend(), 7)
    return v

def test_vector_emplace_back():
    """
    >>> test_vector_emplace_back()
    [0, 7]
    """
    cdef ivector v
    v.emplace_back()
    v.emplace_back(7)
    return v

def test_vector_shrink_to_fit():
    """
    >>> test_vector_shrink_to_fit()
    """
    cdef ivector v
    v.shrink_to_fit()

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
