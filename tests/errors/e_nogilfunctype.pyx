cdef extern from *:
	cdef void f()
	cdef void (*fp)() nogil

fp = f
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors3/e_nogilfunctype.pyx:5:6: Cannot assign type 'void (void)' to 'void (*)(void) nogil'
"""
