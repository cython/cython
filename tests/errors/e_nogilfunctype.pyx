# mode: error
# tag: warnings

cdef extern from *:
    cdef void f()
    cdef void (*fp)() nogil
    ctypedef void (*fp_t)() nogil

fp = f
fp = <fp_t>f

_ERRORS = u"""
9:5: Cannot assign type 'void (void) noexcept' to 'void (*)(void) noexcept nogil'
"""

_WARNINGS = """
10:5: Casting a GIL-requiring function into a nogil function circumvents GIL validation
"""
