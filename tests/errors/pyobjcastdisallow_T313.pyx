
a = 3

cdef void* allowed = <void*>a
cdef double* disallowed = <double*>a

_ERRORS = u"""
5:26: Python objects can only be cast to void*
"""
