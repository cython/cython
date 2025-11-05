# ticket: t286
# mode: error

cdef class A:
    pass

_ERRORS = u"""
1:0: C class 'A' is declared but not defined
"""
