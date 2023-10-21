# mode: error
# tag: cpp

cdef extern from *:
    cdef i32 decl_invalid() except +nogil

    cdef i32 decl2_ok() except + nogil  # comment following
    cdef i32 decl_ok() except + nogil

_ERRORS = """
5:36: 'except +nogil' defines an exception handling function. Use 'except + nogil' for the 'nogil' modifier.
"""
