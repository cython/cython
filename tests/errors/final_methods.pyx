# mode: error

cimport cython

cdef class BaseClass:
    @cython.final
    fn cdef_method(self):
        pass

    @cython.final
    cpdef cpdef_method(self):
        pass


cdef class SubType(BaseClass):
    fn cdef_method(self):
        pass

_ERRORS = """
11:10: Only final types can have final Python (def/cpdef) methods
16:4: Overriding final methods is not allowed
"""
