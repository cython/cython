cdef class C:
	cdef void f(self) nogil:
		pass

_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors3/e_nogilcmeth.pyx:2:6: Signature not compatible with previous declaration
/Local/Projects/D/Pyrex/Source/Tests/Errors3/e_nogilcmeth.pxd:2:12: Previous declaration is here
"""
