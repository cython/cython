cimport cython

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
    import sys
    py_version = sys.version_info[:2]
    if py_version >= (3, 7): # built-in dict is insertion-ordered
        global_values = list(globals().values())
    else:
        global_values = [A, B, C, X, Y, Z]
    for value in global_values:
        if isinstance(value, type):
            print(value.__name__)
