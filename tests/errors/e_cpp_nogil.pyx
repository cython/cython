# mode: error
# tag: cpp

extern from *:
    fn i32 decl_invalid() except +nogil

    fn i32 decl2_ok() except + nogil  # comment following

    fn i32 decl_ok() except + nogil

_ERRORS = """
5:34: 'except +nogil' defines an exception handling function. Use 'except + nogil' for the 'nogil' modifier.
"""
