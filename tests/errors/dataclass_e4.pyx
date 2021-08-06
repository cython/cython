# mode: error

cimport cython

@cython.dataclasses.dataclass
cdef class C:
    a: int = cython.dataclasses.field(unexpected=True)

_ERRORS = """
7:49: cython.dataclasses.field() got an unexpected keyword argument 'unexpected'
"""
