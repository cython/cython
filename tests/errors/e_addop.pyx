# mode: error

def f():
	cdef i32 int1, int3
	cdef i32 *ptr1, *ptr2, *ptr3
	ptr1 = ptr2 + ptr3 # error

_ERRORS = u"""
6:13: Invalid operand types for '+' (int *; int *)
"""
