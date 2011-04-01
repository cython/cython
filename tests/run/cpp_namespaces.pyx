# tag: cpp

cdef extern from "cpp_namespaces_helper.h" namespace "A":
    ctypedef int A_t
    A_t A_func(A_t first, A_t)
    cdef void f(A_t)

cdef extern from "cpp_namespaces_helper.h" namespace "outer":
    int outer_value

cdef extern from "cpp_namespaces_helper.h" namespace "outer::inner":
    int inner_value

def test_function(x, y):
    """
    >>> test_function(1, 2)
    3
    >>> test_function(9, 16)
    25
    """
    return A_func(x, y)

def test_nested():
    """
    >>> test_nested()
    10
    100
    """
    print outer_value
    print inner_value

def test_typedef(A_t a):
    """
    >>> test_typedef(3)
    3
    """
    return a
