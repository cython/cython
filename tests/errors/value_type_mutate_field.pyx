# mode: error
# The frozen-field-write error fires for ANY frozen dataclass (the immutability
# comes from frozen=True, not from value_type).
cimport cython
from dataclasses import dataclass

@cython.value_type
@cython.final
@dataclass(frozen=True)
cdef class Vec:
    x: cython.double

@cython.final
@dataclass(frozen=True)
cdef class Boxed:
    x: cython.double

def mutate_value(Vec v):
    v.x = 5.0

def mutate_boxed(Boxed b):
    b.x = 5.0


_ERRORS = """
19:5: cannot assign to field 'x' of frozen dataclass 'Vec'
22:5: cannot assign to field 'x' of frozen dataclass 'Boxed'
"""
