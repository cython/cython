# mode: error
cimport cython
from dataclasses import dataclass, field

@cython.value_type
@cython.final
@dataclass(frozen=True)
cdef class Vec:
    x: cython.double
    y: cython.double = field(default_factory=float)


_ERRORS = """
5:0: value_type does not support default_factory fields (yet)
"""
