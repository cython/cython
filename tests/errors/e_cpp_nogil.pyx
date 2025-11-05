# mode: error
# tag: cpp

cdef extern from *:
    cdef int decl_invalid() except +nogil

    cdef int decl2_ok() except + nogil  # comment following
    cdef int decl_ok() except + nogil

_ERRORS = """
5:36: 'except +nogil' defines an exception handling function. Use 'except + nogil' for the 'nogil' modifier.
"""
