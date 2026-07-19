# mode: error

cimport cython

@cython.collection_type('sequence')
@cython.collection_type('mapping')
cdef class BothCollection:
    pass

_ERRORS = """
5:0: Multiple values of collection_type are not supported
"""
