cdef int i
i()

cdef float f
f()

ctypedef struct s:    # FIXME: this might be worth an error ...
    int x
s()

cdef int x():
    return 0

x()()

_ERRORS = u"""
2:1: Calling non-function type 'int'
5:1: Calling non-function type 'float'
14:3: Calling non-function type 'int'
"""
