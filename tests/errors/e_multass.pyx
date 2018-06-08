# mode: error

def f(obj1a, obj1b):
	cdef int int1, int2, int3
	cdef int *ptr2
	int1, int3, obj1a = int2, ptr2, obj1b # error


_ERRORS = u"""
6:27: Cannot assign type 'int *' to 'int'
"""
