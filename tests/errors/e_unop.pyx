def f():
	cdef int int1
	cdef char *str2
	int1 = -str2 # error
	int1 = ~str2 # error
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_unop.pyx:4:8: Invalid operand type for '-' (char *)
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_unop.pyx:5:8: Invalid operand type for '~' (char *)
"""
