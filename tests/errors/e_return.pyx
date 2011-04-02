# mode: error

cdef void g():
	cdef int i
	return i # error

cdef int h():
	cdef int *p
	return # error
	return p # error
_ERRORS = u"""
5:17: Return with value in void function
9:1: Return value required
10:17: Cannot assign type 'int *' to 'int'
"""
