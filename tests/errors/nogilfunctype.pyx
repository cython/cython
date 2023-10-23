# mode: error

extern from *:
    let void f()
    let void (*fp)() nogil

    let void g() nogil
    let void (*gp)()

gp = g

fp = f

_ERRORS = u"""
12:5: Cannot assign type 'void (void) noexcept' to 'void (*)(void) noexcept nogil'
"""
