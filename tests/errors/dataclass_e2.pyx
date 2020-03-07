# mode: error
# tag: dataclass

import dataclasses

@dataclasses.dataclass
cdef class C:
    pass

# TODO ideally I'd like some better errors, directing the user towards cython.dataclass
_ERRORS = """
6:0: Cdef functions/classes cannot take arbitrary decorators.
6:0: Use '@cython.dataclass' on cdef classes to create a dataclass
"""
