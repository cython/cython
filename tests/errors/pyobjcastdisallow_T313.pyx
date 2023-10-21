# ticket: t313
# mode: error

a = 3

cdef void* allowed = <void*>a
cdef f64* disallowed = <f64*>a

_ERRORS = u"""
7:23: Python objects cannot be cast to pointers of primitive types
"""
