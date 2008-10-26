cdef int c1 = "t"     # works
cdef int c2 = "te"    # fails
cdef int cx = "test"  # fails

_ERRORS = u"""
2:14: Only coerce single-character ascii strings can be used as ints.
3:14: Only coerce single-character ascii strings can be used as ints.
"""
