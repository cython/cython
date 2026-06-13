# mode: error
cimport cython
from dataclasses import dataclass

@cython.value_type
@cython.final
@dataclass(frozen=True)
cdef extern class mymod.Vec:
    x: cython.double


_ERRORS = """
5:0: value_type classes cannot be declared 'extern' or in a .pxd (cross-module value types are not supported yet)
"""
