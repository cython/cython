cdef object blarg

def foo(obj):
	cdef void *p
	p = <void *>blarg # ok
	p = <void *>(obj + blarg) # error - temporary

_ERRORS = u"""
6:5: Casting temporary Python object to non-numeric non-Python type
"""
