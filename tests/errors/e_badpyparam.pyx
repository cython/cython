cdef struct Foo

def f(Foo *p):
	pass
_ERRORS = u"""
3:6: Cannot convert Python object argument to type 'Foo *'
"""
