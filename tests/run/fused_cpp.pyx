# tag: cpp

cimport cython
from libcpp.vector cimport vector
from libcpp.typeinfo cimport type_info
from cython.operator cimport typeid

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

cdef fused C:
   int
   object

cdef const type_info* tidint = &typeid(int)
def typeid_call(C x):
    """
    For GH issue 3203
    >>> typeid_call(1)
    True
    """
    cdef const type_info* a = &typeid(C)
    return a[0] == tidint[0]

cimport cython

def typeid_call2(cython.integral x):
    """
    For GH issue 3203
    >>> typeid_call2[int](1)
    True
    """
    cdef const type_info* a = &typeid(cython.integral)
    return a[0] == tidint[0]
