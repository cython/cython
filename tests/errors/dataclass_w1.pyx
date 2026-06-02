# mode: compile
# tag: warnings

from dataclass_w1_othermod cimport SomeBase
from cython.dataclasses cimport dataclass

@dataclass
cdef class DC(SomeBase):
    a: str = ""


_WARNINGS = """
7:0: Cannot reliably handle Cython dataclasses with base types in external modules since it is not possible to tell what fields they have
"""
