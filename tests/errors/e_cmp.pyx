cdef void foo():
	cdef int bool, int1
	cdef char *ptr2
	cdef int *ptr3
	bool = int1 == ptr2 # error
	bool = ptr2 == ptr3 # error
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_cmp.pyx:5:13: Invalid types for '==' (int, char *)
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_cmp.pyx:6:13: Invalid types for '==' (char *, int *)
"""
