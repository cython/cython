cdef extern from *:
	cdef void f() nogil
	cdef void (*fp)()

fp = f
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors3/e_nogilfunctype.pyx:5:6: Cannot assign type 'void (void) nogil' to 'void (*)(void)'
"""
