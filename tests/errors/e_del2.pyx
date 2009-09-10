# Errors reported during code generation.

cdef int i

def f(a):
	del a # error: deletion of local name not supported
	del i # error: deletion of local name not supported

_ERRORS = u"""
6:52: Deletion of local or C global name not supported
7:52: Deletion of local or C global name not supported
"""
