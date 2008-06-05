cdef extern from *:
    cdef void f() nogil
    cdef void (*fp)()

fp = f

_ERRORS = u"""
5:6: Cannot assign type 'void (void) nogil' to 'void (*)(void)'
"""
