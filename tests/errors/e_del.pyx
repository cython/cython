# mode: error

cdef struct S:
	int m

def f(a):
	cdef int i, x[2]
	cdef S s
	global j
	del f() # error
	del i # error: deletion of non-Python object
	del j # error: deletion of non-Python object
	del x[i] # error: deletion of non-Python object
	del s.m # error: deletion of non-Python object
_ERRORS = u"""
10:6: Cannot assign to or delete this
11:45: Deletion of non-Python, non-C++ object
13:6: Deletion of non-Python, non-C++ object
14:6: Deletion of non-Python, non-C++ object
"""
