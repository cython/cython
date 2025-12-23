# mode: error

cdef class Test:
    cdef __cinit__(self):
        pass

    cdef __len__(self):
        pass


_ERRORS = u"""
4:4: Special methods must be declared with 'def', not 'cdef'
7:4: Special methods must be declared with 'def', not 'cdef'
"""
