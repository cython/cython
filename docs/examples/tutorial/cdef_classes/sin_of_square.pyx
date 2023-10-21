from libc.math cimport sin

cdef class Function:
    cpdef f64 evaluate(self, f64 x) except *:
        return 0

cdef class SinOfSquareFunction(Function):
    cpdef f64 evaluate(self, f64 x) except *:
        return sin(x ** 2)
