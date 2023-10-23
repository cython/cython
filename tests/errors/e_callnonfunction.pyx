# mode: error

cdef i32 i
i()

cdef f32 f
f()

ctypedef struct s:    # FIXME: this might be worth an error ...
    i32 x
s()

fn i32 x():
    return 0

x()()

_ERRORS = u"""
4:1: Calling non-function type 'int'
7:1: Calling non-function type 'float'
16:3: Calling non-function type 'int'
"""
