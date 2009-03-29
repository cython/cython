cdef void foo():
	cdef int bool, int1
	cdef char *ptr2
	cdef int *ptr3
	bool = int1 == ptr2 # error
	bool = ptr2 == ptr3 # error
_ERRORS = u"""
5:13: Invalid types for '==' (int, char *)
6:13: Invalid types for '==' (char *, int *)
"""
