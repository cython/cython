# This is the Cython version, using cdef to declare C-level attributes.

cdef class A:
    cdef int a, b
    cdef public int c
    cdef int d
    cdef readonly int e

    def __init__(self, a, b, c, d=5, e=3):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e