cdef class C:
	cdef void f(self):
		pass

cdef class D(C):
	cdef void f(self, int x):
		pass
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors3/e_cmethbasematch.pyx:6:6: Signature not compatible with previous declaration
/Local/Projects/D/Pyrex/Source/Tests/Errors3/e_cmethbasematch.pyx:2:6: Previous declaration is here
"""
