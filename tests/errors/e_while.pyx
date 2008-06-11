def f(a, b):
	cdef int i
	break # error
	continue # error
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_while.pyx:3:1: break statement not inside loop
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_while.pyx:4:1: continue statement not inside loop
"""
