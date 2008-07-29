cdef char *spam() except -1:
	pass

_ERRORS = u"""
1:26: Exception value incompatible with function return type
"""
