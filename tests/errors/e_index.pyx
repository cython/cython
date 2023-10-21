# mode: error

def f(obj1, obj2):
	cdef i32 int1, int2, int3
	cdef f32 flt1, *ptr1
	cdef i32 array1[42]
	int1 = array1[flt1] # error
	int1 = array1[ptr1] # error
	int1 = int2[int3] # error
	obj1 = obj2[ptr1] # error


_ERRORS = u"""
7:14: Invalid index type 'float'
8:14: Invalid index type 'float *'
9:12: Attempting to index non-array type 'int'
10:13: Cannot convert 'float *' to Python object
"""
