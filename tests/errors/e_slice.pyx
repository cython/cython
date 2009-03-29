def f(obj2):
	cdef int *ptr1
	obj1 = obj2[ptr1::] # error
	obj1 = obj2[:ptr1:] # error
	obj1 = obj2[::ptr1] # error
_ERRORS = u"""
3:17: Cannot convert 'int *' to Python object
4:18: Cannot convert 'int *' to Python object
5:19: Cannot convert 'int *' to Python object
"""
