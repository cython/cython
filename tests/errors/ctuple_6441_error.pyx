# mode: error

cdef int ctuple_static_index_out_of_range((int, int, int) v):
    return v[3]


_ERRORS = u"""
4:12: Index 3 out of bounds for '(int, int, int)'
"""

# BUG: These should fail on compile

"""cdef int *SHOULD_FAIL_test_index_ctuple_const_addrof():
    return &(<(int, int, int)>(<int>1, <int>2, <int>3))[0]

cdef long *SHOULD_FAIL_test_index_tuple_const_addrof():
    return &(1, 2, 3)[0]"""
