# mode: error

cimport cython

@cython.dataclasses.dataclass
cdef class C:
    a: int = cython.dataclasses.field(unexpected=True)

_ERRORS = """
7:49: 'unexpected' is an invalid keyword argument for cython.dataclasses.field()
"""
