# mode: error

cdef enum Foo:
    d

Foo

_ERRORS = u"""
6:0: 'Foo' is not a constant, variable or function identifier
"""
