# mode: error

cdef enum Spam(i32):
    a, b

_ERRORS = u"""
3:14: Expected ':', found '('
"""
