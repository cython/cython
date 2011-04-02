# mode: error

cdef extern class Grail.Shrubbery

cdef void spam(Shrubbery sh not None):
	pass
_ERRORS = u"""
5:15: 'not None' only allowed in Python functions
"""
