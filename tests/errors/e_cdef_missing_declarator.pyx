cdef int

cdef extern from *:
	void f(int)
_ERRORS = u"""
1:8: Empty declarator
"""
