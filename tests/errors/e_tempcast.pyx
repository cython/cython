cdef object blarg

def foo(obj):
	cdef int *p
	p = <int *>blarg # okay
	p = <int *>(foo + blarg) # error - temporary
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors1/e_tempcast.pyx:6:5: Casting temporary Python object to non-numeric non-Python type
"""
