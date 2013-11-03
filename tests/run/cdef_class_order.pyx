cimport cython

cdef class B

cdef class A(object):
    cdef list dealloc1

cdef class B(A):
    cdef list dealloc2

def test():
    """
    >>> test()
    """
    A(), B()
