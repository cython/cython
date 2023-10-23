# mode: error

cdef int

extern from *:
    void f(i32)

_ERRORS = u"""
3:8: Empty declarator
"""
