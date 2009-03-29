cdef struct S:
	int m

def f(a):
	cdef int i, x[2]
	cdef S s
	global j
	del f() # error
	del i # error: deletion of non-Python object
	del j # error: deletion of non-Python object
	del a # error: deletion of local name not supported
	del x[i] # error: deletion of non-Python object
	del s.m # error: deletion of non-Python object
_ERRORS = u"""
8:6: Cannot assign to or delete this
9:45: Deletion of non-Python object
12:6: Deletion of non-Python object
13:6: Deletion of non-Python object
11:52: Deletion of local or C global name not supported
"""
