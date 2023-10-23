# mode: error

cdef class Test:
    fn __cinit__(self):
        pass

    fn __len__(self):
        pass

_ERRORS = u"""
4:4: Special methods must be declared with 'def', not 'cdef'
7:4: Special methods must be declared with 'def', not 'cdef'
"""
