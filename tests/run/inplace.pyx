__doc__ = u"""
    >>> str(f(5, 7))
    '29509034655744'

    >>> g(13, 4)
    32

    >>> h(56, 7)
    105.0

    >>> arrays()
    19

    >>> attributes()
    26 26 26

    >>> smoketest()
    10
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

cdef class A:
    cdef attr
    cdef int attr2
    cdef char* buf
    def __init__(self):
        self.attr = 3
        self.attr2 = 3

class B:
    attr = 3

def attributes():
    cdef A a = A()
    b = B()
    a.attr += 10
    a.attr *= 2
    a.attr2 += 10
    a.attr2 *= 2
    b.attr += 10
    b.attr *= 2
    print a.attr, a.attr2, b.attr

def get_2(): return 2
cdef int identity(int value): return value

def smoketest():
    cdef char* buf = <char*>stdlib.malloc(10)
    cdef A a = A()
    a.buf = buf
    a.buf[identity(1)] = 0
    (a.buf + identity(4) - <int>(2*get_2() - 1))[get_2() - 2*identity(1)] += 10
    print a.buf[1]
    stdlib.free(buf)

