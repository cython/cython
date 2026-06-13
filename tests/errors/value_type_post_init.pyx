# mode: error
cimport cython
from dataclasses import dataclass

@cython.value_type
@cython.final
@dataclass(frozen=True)
cdef class Vec:
    x: cython.double
    def __post_init__(self):
        pass


_ERRORS = """
5:0: value_type classes cannot define __post_init__
"""
