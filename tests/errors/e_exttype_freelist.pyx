# mode: error
# tag: freelist, werror

cimport cython

@cython.freelist(8)
cdef class ExtType:
    pass

@cython.freelist(8)
cdef class ExtTypeObject(object):
    pass

cdef class ExtSubTypeOk(ExtType):
    pass

@cython.freelist(8)
cdef class ExtSubTypeFail(ExtType):
    pass


_ERRORS = """
17:0: freelists cannot be used on subtypes, only the base class can manage them
"""
