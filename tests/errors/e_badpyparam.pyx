# mode: error

cdef struct Foo

def f(Foo *p):
	pass
_ERRORS = u"""
5:6: Cannot convert Python object argument to type 'Foo *'
"""
