# mode: error

cdef int c1 = "t"     # works
cdef int c2 = "te"    # fails
cdef int cx = "test"  # fails

cdef int x1 =  "\xFF"    # works
cdef int x2 =  "\u0FFF"  # fails

cdef Py_UNICODE u1 = u"\xFF"   # works
cdef int u3 = u"\xFF"          # fails


_ERRORS = """
4:14: Only single-character string literals can be coerced into ints.
5:14: Only single-character string literals can be coerced into ints.
8:15: Only single-character string literals can be coerced into ints.
11:14: Unicode literals do not support coercion to C types other than Py_UNICODE/Py_UCS4 (for characters) or Py_UNICODE* (for strings).
"""
