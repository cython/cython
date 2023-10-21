# mode: error

cdef i32 c1 = "t"     # works
cdef i32 c2 = "te"    # fails
cdef i32 cx = "test"  # fails

cdef i32 x1 =  "\xFF"    # works
cdef i32 x2 =  "\u0FFF"  # fails

cdef Py_UNICODE u1 = u"\xFF"   # works
cdef i32 u3 = u"\xFF"          # fails


_ERRORS = """
4:14: Only single-character string literals can be coerced into ints.
5:14: Only single-character string literals can be coerced into ints.
8:15: Only single-character string literals can be coerced into ints.
11:14: Unicode literals do not support coercion to C types other than Py_UNICODE/Py_UCS4 (for characters) or Py_UNICODE* (for strings).
"""
