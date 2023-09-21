# mode: error
from cython cimport view

def main():
    # VALID
    cdef int[::view.indirect, ::1, :] a
    cdef int[::view.indirect, :, ::1] b
    cdef int[::view.indirect_contiguous, ::1, :] c

    # INVALID
    cdef int[::view.contiguous, ::view.indirect, :] d
    cdef int[::1, ::view.indirect, :] e

_ERRORS = u"""
11:12: Only dimension 2 may be contiguous and direct
12:12: Indirect dimension may not follow Fortran contiguous dimension
"""
