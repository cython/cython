# mode: error
cimport cython
from dataclasses import dataclass

@cython.value_type
@cython.final
@dataclass(frozen=True)
cdef class Vec:
    x: cython.double

cdef class Sub(Vec):
    pass


_ERRORS = """
11:15: 'Vec' is not an extension type
"""
