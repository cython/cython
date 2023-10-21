cdef class Function:
    cpdef f64 evaluate(self, f64 x) except *:
        return 0
