__doc__ = u"""
    >>> str(f(5, 7))
    '29509034655744'

    >>> g(13, 4)
    32

    >>> h(56, 7)
    105.0

    >>> arrays()
    19
"""

def f(a,b):
    a += b
    a *= b
    a **= b
    return a

def g(int a, int b):
    a -= b
    a /= b
    a <<= b
    return a

def h(double a, double b):
    a /= b
    a += b
    a *= b
    return a

cimport stdlib

def arrays():
    cdef char* buf = <char*>stdlib.malloc(10)
    cdef int i = 2
    cdef object j = 2
    buf[2] = 0
    buf[i] += 2
    buf[2] *= 10
    buf[j] -= 1
    print buf[2]
    stdlib.free(buf)
