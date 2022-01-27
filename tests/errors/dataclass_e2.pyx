# mode: error
# tag: dataclass

import dataclasses

@dataclasses.dataclass
cdef class C:
    pass

_ERRORS = """
6:0: Cdef functions/classes cannot take arbitrary decorators.
6:0: Use '@cython.dataclasses.dataclass' on cdef classes to create a dataclass
"""
