cdef void foo(obj):
	cdef int i1
	cdef char *p1
	cdef int *p2
	i1 = p1 # error
	p2 = obj # error
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_ass.pyx:5:16: Cannot assign type 'char *' to 'int'
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_ass.pyx:6:17: Cannot convert Python object to 'int *'
"""
