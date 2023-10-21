# mode: error

cdef int

cdef extern from *:
	void f(i32)
_ERRORS = u"""
3:8: Empty declarator
"""
