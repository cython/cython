# mode: error

cdef object x

struct Spam:
    object parrot

def f():
    let Spam s
    s.parrot = x

_ERRORS = u"""
6:11: C struct/union member cannot be a Python object
"""
