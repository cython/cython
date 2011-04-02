# mode: error

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
4:1: Calling non-function type 'int'
7:1: Calling non-function type 'float'
16:3: Calling non-function type 'int'
"""
