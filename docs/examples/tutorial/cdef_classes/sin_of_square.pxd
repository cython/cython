cdef class Function:
    cpdef double evaluate(self, double x) except *

cdef class SinOfSquareFunction(Function):
    cpdef double evaluate(self, double x) except *
