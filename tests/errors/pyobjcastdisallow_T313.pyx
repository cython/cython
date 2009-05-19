
a = 3

cdef void* allowed = <void*>a
cdef double* disallowed = <double*>a

_ERRORS = u"""
5:26: Python objects cannot be casted to pointers of primitive types
"""
