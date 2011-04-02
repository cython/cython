# mode: error

def f():
	cdef int int1, int3
	cdef int *ptr1, *ptr2, *ptr3
	ptr1 = ptr2 + ptr3 # error

_ERRORS = u"""
6:13: Invalid operand types for '+' (int *; int *)
"""
