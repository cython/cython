# tag: cpp

cimport cython
from libcpp.vector cimport vector

def test_cpp_specialization(cython.floating element):
    """
    >>> import cython
    >>> test_cpp_specialization[cython.float](10.0)
    vector[float] * float 10.0
    >>> test_cpp_specialization[cython.double](10.0)
    vector[double] * double 10.0
    """
    cdef vector[cython.floating] *v = new vector[cython.floating]()
    v.push_back(element)
    print cython.typeof(v), cython.typeof(element), v.at(0)
