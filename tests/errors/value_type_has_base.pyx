# mode: error
cimport cython
from dataclasses import dataclass

cdef class Base:
    pass

@cython.value_type
@cython.final
@dataclass(frozen=True)
cdef class Vec(Base):
    x: cython.double


_ERRORS = """
8:0: value_type classes cannot have base classes
"""
