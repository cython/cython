ctypedef fused NotInPy:
    int
    float

cdef class TestCls:
    cpdef cpfunc(self, NotInPy arg)
