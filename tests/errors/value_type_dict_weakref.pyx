# mode: error
cimport cython
from dataclasses import dataclass

@cython.value_type
@cython.final
@dataclass(frozen=True)
cdef class Vec:
    x: cython.double
    cdef dict __dict__


_ERRORS = """
10:14: value_type field '__dict__' must be a C type (int/float/bool/enum/ctuple/nested value type), not a Python object
5:0: value_type classes cannot have __dict__ or __weakref__
"""
