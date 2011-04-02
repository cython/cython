# mode: error

cdef void spam():
	None = 42
_ERRORS = u"""
4:1: Cannot assign to or delete this
"""
