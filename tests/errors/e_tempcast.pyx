# mode: error

cdef object blarg

def foo(obj):
	cdef void *p
	p = <void *>blarg # ok
	p = <void *>(obj + blarg) # error - temporary

_ERRORS = u"""
8:5: Casting temporary Python object to non-numeric non-Python type
8:5: Storing unsafe C derivative of temporary Python reference
"""
