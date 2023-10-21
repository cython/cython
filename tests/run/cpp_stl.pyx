# mode: run
# tag: cpp, werror

cdef extern from "vector" namespace "std":
    cdef cppclass vector[T]:
        T at(i32)
        void push_back(T t)
        void assign(i32, T)
        void clear()
        i32 size()

        cppclass iterator:
            T operator*()
            iterator operator++()
            bint operator==(iterator)
            bint operator!=(iterator)

        iterator end()
        iterator begin()

from cython.operator cimport dereference as deref, preincrement as inc

def test_vector(L):
    """
    >>> test_vector([1,10,100])
    1
    10
    100
    """
    v = new vector[i32]()
    for a in L:
        v.push_back(a)
    cdef i32 i
    for i in range(len(L)):
        print v.at(i)
    del v

ctypedef i32 my_int
def test_vector_typedef(L):
    """
    >>> test_vector_typedef([1, 2, 3])
    [1, 2, 3]
    """
    cdef vector[my_int] v = L
    cdef vector[i32] vv = v
    return vv

def test_vector_iterator(L):
    """
    >>> test_vector([11, 37, 389, 5077])
    11
    37
    389
    5077
    """
    v = new vector[i32]()
    for a in L:
        v.push_back(a)
    cdef vector[i32].iterator iter = v.begin()
    while iter != v.end():
        print deref(iter)
        inc(iter)
    del v

cdef class VectorWrapper:
    """
    >>> VectorWrapper(1, .5, .25, .125)
    [1.0, 0.5, 0.25, 0.125]
    """
    cdef vector[f64] vector
    def __init__(self, *args):
        self.vector = args
    def __repr__(self):
        return repr(self.vector)
