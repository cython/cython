# mode: error
from cython.cimports.cython import view

def main():
    # VALID
    a: cython.int[::view.indirect, ::1, :]
    b: cython.int[::view.indirect, :, ::1]
    c: cython.int[::view.indirect_contiguous, ::1, :]

    # INVALID
    d: cython.int[::view.contiguous, ::view.indirect, :]
    e: cython.int[::1, ::view.indirect, :]

_ERRORS = u"""
12:17: Only dimension 2 may be contiguous and direct
"""
