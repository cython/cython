cdef class Function:
    cpdef f64 evaluate(self, f64 x) except *

cdef class SinOfSquareFunction(Function):
    cpdef f64 evaluate(self, f64 x) except *
