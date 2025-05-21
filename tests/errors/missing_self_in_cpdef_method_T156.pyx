# ticket: t156
# mode: error

cdef class B:
    cpdef b():
        pass


_ERRORS = u"""
5:4: C method has no self argument
"""
