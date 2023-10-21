# mode: error

from cython cimport view

def main():
    # VALID
    cdef i32[::view.indirect, ::1, :] a
    cdef i32[::view.indirect, :, ::1] b
    cdef i32[::view.indirect_contiguous, ::1, :] c

    # INVALID
    cdef i32[::view.contiguous, ::view.indirect, :] d
    cdef i32[::1, ::view.indirect, :] e

_ERRORS = u"""
12:12: Only dimension 2 may be contiguous and direct
13:12: Indirect dimension may not follow Fortran contiguous dimension
"""
