# mode: error

from cython cimport view

def main():
    # VALID
    let i32[::view.indirect, ::1, :] a
    let i32[::view.indirect, :, ::1] b
    let i32[::view.indirect_contiguous, ::1, :] c

    # INVALID
    let i32[::view.contiguous, ::view.indirect, :] d
    let i32[::1, ::view.indirect, :] e

_ERRORS = u"""
12:11: Only dimension 2 may be contiguous and direct
13:11: Indirect dimension may not follow Fortran contiguous dimension
"""
