def f():
	cdef int int2
	cdef char *ptr1, *ptr2, *ptr3
	ptr1 = int2 - ptr3 # error
	ptr1 = ptr2 - ptr3 # error
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_subop.pyx:4:13: Invalid operand types for '-' (int; char *)
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_subop.pyx:5:13: Cannot assign type 'int' to 'char *'
"""
