__doc__ = u"""
    >>> str(f(5, 7))
    '29509034655744'

"""

def f(a,b):
    a += b
    a *= b
    a **= b
    return a

def g(int a, int b):
    """
    >>> g(13, 4)
    32
    """
    a -= b
    a /= b
    a <<= b
    return a

def h(double a, double b):
    """
    >>> h(56, 7)
    105.0
    """
    a /= b
    a += b
    a *= b
    return a

cimport stdlib

def arrays():
    """
    >>> arrays()
    19
    """
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
    """
    >>> attributes()
    26 26 26
    """
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
    """
    >>> smoketest()
    10
    """
    cdef char* buf = <char*>stdlib.malloc(10)
    cdef A a = A()
    a.buf = buf
    a.buf[identity(1)] = 0
    (a.buf + identity(4) - <int>(2*get_2() - 1))[get_2() - 2*identity(1)] += 10
    print a.buf[1]
    stdlib.free(buf)


def side_effect(x):
    print u"side effect", x
    return x
    
cdef int c_side_effect(int x):
    print u"c side effect", x
    return x
    
def test_side_effects():
    """
    >>> test_side_effects()
    side effect 1
    c side effect 2
    side effect 3
    c side effect 4
    ([0, 11, 102, 3, 4], [0, 1, 2, 13, 104])
    """
    a = list(range(5))
    a[side_effect(1)] += 10
    a[c_side_effect(2)] += 100
    cdef int i
    cdef int b[5]
    for i from 0 <= i < 5:
        b[i] = i
    b[side_effect(3)] += 10
    b[c_side_effect(4)] += 100
    return a, [b[i] for i from 0 <= i < 5]
