cdef object blarg

def foo(obj):
	cdef int *p
	p = <int *>blarg # okay
	p = <int *>(foo + blarg) # error - temporary
_ERRORS = u"""
6:5: Casting temporary Python object to non-numeric non-Python type
"""
