# A genuine hand-written .pxd with @value_type.
# This must produce a compile error: value_type is not supported in
# hand-written .pxd files; use --cimport-from-pyx instead.
cimport cython
from dataclasses import dataclass

@cython.value_type
@cython.final
@dataclass(frozen=True)
cdef class Vec2:
    cdef double x
    cdef double y
