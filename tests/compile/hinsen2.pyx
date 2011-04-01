# mode: compile

cdef class vector:
    def __div__(vector self, double factor):
        cdef object result = vector()
        return result
