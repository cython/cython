# mode: error
cimport cython
from dataclasses import dataclass

@cython.value_type
@cython.final
@dataclass
cdef class Vec:
    x: cython.double


_ERRORS = """
5:0: value_type requires '@dataclass(frozen=True)'
"""
