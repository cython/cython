# mode: error

cdef class C:
    cdef void f(self):
        pass

_ERRORS = u"""
2:15: Previous declaration is here
4:9: Signature not compatible with previous declaration
"""
