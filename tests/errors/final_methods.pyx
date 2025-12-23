# mode: error

cimport cython

cdef class BaseClass:
    @cython.final
    cdef cdef_method(self):
        pass

    @cython.final
    cpdef cpdef_method(self):
        pass


cdef class SubType(BaseClass):
    cdef cdef_method(self):
        pass


_ERRORS = """
10:4: Only final types can have final Python (def/cpdef) methods
16:4: Overriding final methods is not allowed
"""
