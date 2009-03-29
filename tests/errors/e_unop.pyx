def f():
	cdef int int1
	cdef char *str2
	int1 = -str2 # error
	int1 = ~str2 # error
_ERRORS = u"""
4:8: Invalid operand type for '-' (char *)
5:8: Invalid operand type for '~' (char *)
"""
