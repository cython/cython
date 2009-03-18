cdef int c1 = "t"     # works
cdef int c2 = "te"    # fails
cdef int cx = "test"  # fails

cdef int x1 =  "\xFF"    # works
cdef int x2 = u"\xFF"    # fails


_ERRORS = u"""
2:14: Only single-character byte strings can be coerced into ints.
3:14: Only single-character byte strings can be coerced into ints.
6:14: Unicode objects do not support coercion to C types.
"""
