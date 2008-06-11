def f(obj2):
	cdef int *ptr1
	obj1 = obj2[ptr1::] # error
	obj1 = obj2[:ptr1:] # error
	obj1 = obj2[::ptr1] # error
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_slice.pyx:3:17: Cannot convert 'int *' to Python object
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_slice.pyx:4:18: Cannot convert 'int *' to Python object
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_slice.pyx:5:19: Cannot convert 'int *' to Python object
"""
