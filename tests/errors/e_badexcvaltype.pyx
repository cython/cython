# mode: error

cdef char *spam() except -1:
	pass

_ERRORS = u"""
3:26: Cannot assign type 'long' to 'char *'
3:26: Exception value incompatible with function return type
"""
