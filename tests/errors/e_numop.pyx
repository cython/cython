# mode: error

def f():
	cdef int int1, int2
	cdef int *ptr
	int1 = int2 * ptr # error
_ERRORS = u"""
6:13: Invalid operand types for '*' (int; int *)
"""
