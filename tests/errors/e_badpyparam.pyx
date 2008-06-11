cdef struct Foo

def f(Foo *p):
	pass
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_badpyparam.pyx:3:6: Cannot convert Python object argument to type 'Foo *'
"""
