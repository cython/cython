def f(a, b):
	cdef int i
	break # error
	continue # error
_ERRORS = u"""
3:1: break statement not inside loop
4:1: continue statement not inside loop
"""
