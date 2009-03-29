def f():
	cdef int int2
	cdef char *ptr1, *ptr2, *ptr3
	ptr1 = int2 - ptr3 # error
	ptr1 = ptr2 - ptr3 # error
_ERRORS = u"""
4:13: Invalid operand types for '-' (int; char *)
5:13: Cannot assign type 'int' to 'char *'
"""
