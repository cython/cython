cdef class A:
    cdef int value = 3

_ERRORS = u"""
2:13: Cannot assign default value to cdef class attributes
"""
