# mode: error

fn char *spam() except -1:
	pass

_ERRORS = u"""
3:24: Cannot assign type 'long' to 'char *'
3:24: Exception value incompatible with function return type
"""
