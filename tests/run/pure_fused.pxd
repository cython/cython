import cython

ctypedef fused NotInPy:
    int
    float

cdef class TestCls:
    @cython.locals(loca = NotInPy)
    cpdef cpfunc(self, NotInPy arg)
