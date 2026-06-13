# mode: error
cimport cython
from dataclasses import dataclass

@cython.value_type
@cython.final
@dataclass(frozen=True)
cdef class Vec:
    x: object


_ERRORS = """
9:4: value_type field 'x' must be a C type (int/float/bool/enum/ctuple/nested value type), not a Python object
"""
