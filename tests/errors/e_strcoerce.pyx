cdef int c1 = "t"     # works
cdef int c2 = "te"    # fails
cdef int cx = "test"  # fails

cdef int x1 =  "\xFF"    # works
cdef int x2 =  "\u0FFF"  # fails

cdef Py_UNICODE u1 = u"\xFF"   # works
cdef int u3 = u"\xFF"          # fails


_ERRORS = """
2:14: Only single-character string literals can be coerced into ints.
3:14: Only single-character string literals can be coerced into ints.
6:15: Only single-character string literals can be coerced into ints.
9:14: Unicode literals do not support coercion to C types other than Py_UNICODE or Py_UCS4.
"""
