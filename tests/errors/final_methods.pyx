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
11:10: Only final type could have final cpdef method
16:9: Overriding final methods is not allowed
"""
