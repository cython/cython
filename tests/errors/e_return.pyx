# cython: remove_unreachable=False
# mode: error

cdef void g():
	cdef int i
	return i # error

cdef int h():
	cdef int *p
	return # error
	return p # error


_ERRORS = u"""
6:8: Return with value in void function
10:1: Return value required
11:8: Cannot assign type 'int *' to 'int'
"""
