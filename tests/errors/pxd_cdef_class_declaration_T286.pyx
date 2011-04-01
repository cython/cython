# ticket: 286
# mode: error

cdef class A:
    pass

_ERRORS = u"""
1:5: C class 'A' is declared but not defined
"""
