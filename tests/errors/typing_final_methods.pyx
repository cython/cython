# mode: error

# typing.final must produce the same method-level errors as cython.final.

from typing import final


cdef class BaseClass:
    @final
    cdef cdef_method(self):
        pass

    @final
    cpdef cpdef_method(self):
        pass


cdef class SubType(BaseClass):
    cdef cdef_method(self):
        pass


_ERRORS = """
13:4: Only final types can have final Python (def/cpdef) methods
19:4: Overriding final methods is not allowed
"""
