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
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_del.pyx:8:6: Cannot assign to or delete this
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_del.pyx:9:45: Deletion of non-Python object
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_del.pyx:12:6: Deletion of non-Python object
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_del.pyx:13:6: Deletion of non-Python object
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_del.pyx:11:52: Deletion of local or C global name not supported
"""
