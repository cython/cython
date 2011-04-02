# mode: error

cdef void foo():
	cdef int bool, int1
	cdef char *ptr2
	cdef int *ptr3
	cdef object i = 5

	bool = i == ptr2  # evaluated in Python space
	bool = ptr3 == i # error
	bool = int1 == ptr2 # error
	bool = ptr2 == ptr3 # error

	bool = 1 in 2 in 3

_ERRORS = u"""
10:13: Invalid types for '==' (int *, Python object)
11:13: Invalid types for '==' (int, char *)
12:13: Invalid types for '==' (char *, int *)
"""
