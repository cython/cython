cdef int c1 = "t"     # works
cdef int c2 = "te"    # fails
cdef int cx = "test"  # fails

cdef int x1 =  "\xFF"    # works
cdef int x2 =  "\u0FFF"  # fails
cdef int x3 = u"\xFF"    # fails


_ERRORS = u"""
2:14: Only single-character strings can be coerced into ints.
3:14: Only single-character strings can be coerced into ints.
6:15: Only single-character strings can be coerced into ints.
7:14: Unicode objects do not support coercion to C types.
"""
