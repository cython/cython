cdef extern from "<vector>" namespace std:

    cdef cppclass vector[T]:
        void push_back(T)
        size_t size()

def simple_test(double x):
    """
    >>> simple_test(55)
    3
    """
    cdef vector[double] *v 
    try:
        v = new vector[double]()
        v.push_back(1.0)
        v.push_back(x)
        from math import pi
        v.push_back(pi)
        return v.size()
    finally:
        del v

def list_test(L):
    """
    >>> list_test([1,2,4,8])
    (4, 4)
    >>> list_test([])
    (0, 0)
    >>> list_test([-1] * 1000)
    (1000, 1000)
    """
    cdef vector[int] *v 
    try:
        v = new vector[int]()
        for a in L:
            v.push_back(a)
        return len(L), v.size()
    finally:
        del v
