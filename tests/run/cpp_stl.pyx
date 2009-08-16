__doc__ = u"""
    >>> test_vector([1,10,100])
    1
    10
    100
"""

cdef extern from "vector" namespace std:

    cdef cppclass iterator[T]:
        pass

    cdef cppclass vector[T]:
        #constructors
        __init__()

        T at(int)
        void push_back(T t)
        void assign(int, T)
        void clear()

        iterator end()
        iterator begin()

        int size()

def test_vector(L):
    cdef vector[int] *V = new vector[int]()
    for a in L:
        V.push_back(a)
    cdef int i
    for i in range(len(L)):
        print V.at(i)
    del V
