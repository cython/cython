# mode: run
# tag: cpp, error

cdef extern from *:
    cdef int decl_ok() except + nogil
    cdef int decl_invalid() except +nogil

_ERRORS = """
6:41: 'except +nogil' defines an exception handling function. Use 'except + nogil' for the 'nogil' modifier.
"""
