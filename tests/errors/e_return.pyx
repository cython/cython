cdef void g():
	cdef int i
	return i # error

cdef int h():
	cdef int *p
	return # error
	return p # error
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_return.pyx:3:17: Return with value in void function
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_return.pyx:7:1: Return value required
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_return.pyx:8:17: Cannot assign type 'int *' to 'int'
"""
