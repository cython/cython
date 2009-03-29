cdef void g():
	cdef int i
	return i # error

cdef int h():
	cdef int *p
	return # error
	return p # error
_ERRORS = u"""
3:17: Return with value in void function
7:1: Return value required
8:17: Cannot assign type 'int *' to 'int'
"""
