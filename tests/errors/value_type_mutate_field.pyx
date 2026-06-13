# mode: error
cimport cython
from dataclasses import dataclass

@cython.value_type
@cython.final
@dataclass(frozen=True)
cdef class Vec:
    x: cython.double

def mutate(Vec v):
    v.x = 5.0


_ERRORS = """
12:5: cannot assign to field 'x' of frozen value type 'Vec'
"""
