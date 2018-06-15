from libc.math cimport sin

cdef class Function:
    cpdef double evaluate(self, double x) except *:
        return 0

cdef class SinOfSquareFunction(Function):
    cpdef double evaluate(self, double x) except *:
        return sin(x ** 2)
