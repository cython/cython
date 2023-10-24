# mode: error

struct Foo

ctypedef struct Foo:
    i32 i

ctypedef struct Blarg:
    char c

struct Blarg

cdef Foo f
cdef Blarg b

_ERRORS = u"""
5:0: 'Foo' previously declared using 'cdef'
11:0: 'Blarg' previously declared using 'ctypedef'
"""
