cdef char *spam() except -1:
	pass

_ERRORS = u"""
1:26: Cannot assign type 'long' to 'char *'
1:26: Exception value incompatible with function return type
"""
