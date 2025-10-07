# mode: error

cdef extern from *:
    cdef void f()
    cdef void (*fp)() nogil

    cdef void g() nogil
    cdef void (*gp)()

gp = g

fp = f

_ERRORS = u"""
12:5: Cannot assign type 'void (void) noexcept' to 'void (*)(void) noexcept nogil'
"""
