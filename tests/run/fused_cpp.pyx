# tag: cpp

cimport cython
from libcpp.vector cimport vector
from libcpp.map cimport map
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

cdef fused_ref(cython.integral& x):
    return x*2

def test_fused_ref(int x):
    """
    >>> test_fused_ref(5)
    (10, 10)
    """
    return fused_ref(x), fused_ref[int](x)

ctypedef fused nested_fused:
    vector[cython.integral]

cdef vec_of_fused(nested_fused v):
    x = v[0]
    return cython.typeof(x)

def test_nested_fused():
    """
    >>> test_nested_fused()
    int
    long
    """
    cdef vector[int] vi = [0,1]
    cdef vector[long] vl = [0,1]
    print vec_of_fused(vi)
    print vec_of_fused(vl)

ctypedef fused nested_fused2:
    map[cython.integral, cython.floating]

cdef map_of_fused(nested_fused2 m):
    for pair in m:
        return cython.typeof(pair.first), cython.typeof(pair.second)

def test_nested_fused2():
    """
    >>> test_nested_fused2()
    ('int', 'float')
    ('long', 'double')
    """
    cdef map[int, float] mif = { 0: 0.0 }
    cdef map[long, double] mld = { 0: 0.0 }
    print map_of_fused(mif)
    print map_of_fused(mld)
