# mode: error

from cython.dataclasses cimport dataclass

@dataclass
cdef class BaseDataclass:
    a: str = "value"

@dataclass
cdef class MainDataclass(BaseDataclass):
    a: str = "new value"

cdef class Intermediate(BaseDataclass):
    pass

@dataclass
cdef class AnotherDataclass(Intermediate):
    a: str = "ooops"

_ERRORS = """
11:4: Cannot redeclare inherited fields in Cython dataclasses
18:4: Cannot redeclare inherited fields in Cython dataclasses
"""
