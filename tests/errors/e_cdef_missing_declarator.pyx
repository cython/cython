cdef int

cdef extern from *:
	void f(int)
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors3/e_cdef_missing_declarator.pyx:1:8: Empty declarator
"""
