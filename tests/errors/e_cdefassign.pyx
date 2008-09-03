cdef class A:
    cdef int value = 3

cdef extern from *:
    cdef struct B:
        int value = 3

_ERRORS = u"""
2:13: Cannot assign default value to fields in cdef classes, structs or unions
6:12: Cannot assign default value to fields in cdef classes, structs or unions
"""
