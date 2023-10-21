# mode: error

def f():
	cdef i32 int1, int2
	cdef char *ptr
	int1 = int2 | ptr # error
_ERRORS = u"""
6:13: Invalid operand types for '|' (int; char *)
"""
