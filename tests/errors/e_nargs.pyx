cdef extern grail(char *s, int i)
cdef extern spam(char *s, int i,...)

cdef f():
	grail() # too few args
	grail("foo") # too few args
	grail("foo", 42, 17) # too many args
	spam() # too few args
	spam("blarg") # too few args
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_nargs.pyx:5:6: Call with wrong number of arguments (expected 2, got 0)
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_nargs.pyx:6:6: Call with wrong number of arguments (expected 2, got 1)
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_nargs.pyx:7:6: Call with wrong number of arguments (expected 2, got 3)
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_nargs.pyx:8:5: Call with wrong number of arguments (expected at least 2, got 0)
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_nargs.pyx:9:5: Call with wrong number of arguments (expected at least 2, got 1)
"""
