cdef class B

cdef class A(object):
    cdef list dealloc1

cdef class Y(X): pass
cdef class X(C): pass
cdef class C: pass

cdef class B(A):
    cdef list dealloc2

cdef class Z(A): pass


def test():
    """
    >>> test()
    A
    B
    C
    X
    Y
    Z
    """
    A(), B(), C(), X(), Y(), Z()
    for value in list(globals().values()):
        if isinstance(value, type):
            print(value.__name__)
