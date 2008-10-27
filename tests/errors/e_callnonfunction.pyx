cdef int i
i()

cdef float f
f()

ctypedef struct s:    # FIXME: this might be worth an error ...
    int x
s()

_ERRORS = u"""
2:1: Calling non-function type 'int'
5:1: Calling non-function type 'float'
"""
