cdef extern from "vector" namespace "std":

    cdef cppclass vector[T]:

        T at(int)
        void push_back(T t)
        void assign(int, T)
        void clear()
        int size()

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
    v = new vector[int]()
    for a in L:
        v.push_back(a)
    cdef int i
    for i in range(len(L)):
        print v.at(i)
    del v

def test_vector_iterator(L):
    """
    >>> test_vector([11, 37, 389, 5077])
    11
    37
    389
    5077
    """
    v = new vector[int]()
    for a in L:
        v.push_back(a)
    cdef vector[int].iterator iter = v.begin()
    while iter != v.end():
        print deref(iter)
        inc(iter)
    del v
