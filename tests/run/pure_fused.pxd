cimport cython

ctypedef fused NotInPy:
    int
    float

cdef class TestCls:
    @cython.locals(loc = NotInPy)
    cpdef cpfunc(self, NotInPy arg)
