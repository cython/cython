# mode: compile
# tag: dataclass, warnings

cimport cython
from dataclass import field

@cython.dataclasses.dataclass
cdef class E:
    a: int = field()

_WARNINGS="""
9:18: Do you mean cython.dataclasses.field instead?
"""
