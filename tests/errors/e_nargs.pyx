# mode: error

cdef extern grail(char *s, int i)
cdef extern spam(char *s, int i,...)

cdef f():
	grail() # too few args
	grail("foo") # too few args
	grail("foo", 42, 17) # too many args
	spam() # too few args
	spam("blarg") # too few args
_ERRORS = u"""
7:6: Call with wrong number of arguments (expected 2, got 0)
8:6: Call with wrong number of arguments (expected 2, got 1)
9:6: Call with wrong number of arguments (expected 2, got 3)
10:5: Call with wrong number of arguments (expected at least 2, got 0)
11:5: Call with wrong number of arguments (expected at least 2, got 1)
"""
