def f(obj1, obj2):
	cdef int int1, int2, int3
	cdef float flt1, *ptr1
	cdef int array1[42]
	int1 = array1[flt1] # error
	int1 = array1[ptr1] # error
	int1 = int2[int3] # error
	obj1 = obj2[ptr1] # error
_ERRORS = u"""
5:14: Invalid index type 'float'
6:14: Invalid index type 'float *'
7:12: Attempting to index non-array type 'int'
8:17: Cannot convert 'float *' to Python object
"""
