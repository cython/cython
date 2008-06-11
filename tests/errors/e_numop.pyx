def f():
	cdef int int1, int2
	cdef int *ptr
	int1 = int2 * ptr # error
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_numop.pyx:4:13: Invalid operand types for '*' (int; int *)
"""
