# mode: error

cimport cython

cdef class TestClass:
    def foo(self):
        with cython.c_string_encoding("ascii"):
            return


### FIXME: way to many errors for my taste...

_ERRORS = """
7:13: The c_string_encoding compiler directive is not allowed in with statement scope
7:19: 'c_string_encoding' not a valid cython language construct
7:19: 'c_string_encoding' not a valid cython attribute or is being used incorrectly
"""
