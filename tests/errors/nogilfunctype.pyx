cdef extern from *:
    cdef void f()
    cdef void (*fp)() nogil

    cdef void g() nogil
    cdef void (*gp)()

gp = g

fp = f

_ERRORS = u"""
10:6: Cannot assign type 'void (void)' to 'void (*)(void) nogil'
"""
