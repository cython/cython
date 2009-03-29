cdef extern from *:
	cdef void f()
	cdef void (*fp)() nogil

fp = f
_ERRORS = u"""
5:6: Cannot assign type 'void (void)' to 'void (*)(void) nogil'
"""
