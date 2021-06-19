 
cdef class Function:

    cpdef double evaluate(self, double x) except *:
        return 0
