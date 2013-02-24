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
18:5: freelists are not currently supported for subtypes
"""
