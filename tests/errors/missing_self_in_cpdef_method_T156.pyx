
cdef class B:
    cpdef b():
        pass

_ERRORS = u"""
3:10: C method has no self argument
"""
