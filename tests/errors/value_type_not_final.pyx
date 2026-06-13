# mode: error
cimport cython
from dataclasses import dataclass

@cython.value_type
@dataclass(frozen=True)
cdef class Vec:
    x: cython.double


_ERRORS = """
5:0: value_type requires an explicitly 'final' class
"""
