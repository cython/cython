# mode: error

def f(a, b):
	cdef int i
	break # error
	continue # error
_ERRORS = u"""
5:1: break statement not inside loop
6:1: continue statement not inside loop
"""
