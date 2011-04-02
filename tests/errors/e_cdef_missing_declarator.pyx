# mode: error

cdef int

cdef extern from *:
	void f(int)
_ERRORS = u"""
3:8: Empty declarator
"""
