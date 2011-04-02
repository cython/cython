# mode: error

cdef struct Foo

ctypedef struct Foo:
	int i

ctypedef struct Blarg:
	char c

cdef struct Blarg

cdef Foo f
cdef Blarg b

_ERRORS = u"""
5:0: 'Foo' previously declared using 'cdef'
11:5: 'Blarg' previously declared using 'ctypedef'
"""
