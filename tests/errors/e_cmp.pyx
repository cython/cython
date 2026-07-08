# mode: error

import cython

cdef void foo():
    cdef int bool, int1
    cdef char *ptr2
    cdef int *ptr3
    cdef object i = 5

    bool = i == ptr2  # evaluated in Python space
    bool = ptr3 == i # error
    bool = int1 == ptr2 # error
    bool = ptr2 == ptr3 # error

    bool = 1 in 2 in 3


cdef void likely_foo(int j):
    cdef bint bol
    cdef int i = 5

    bol = cython.likely(i == j)
    bol = cython.unlikely(i == j)
    a = i if cython.likely(j > 5) else -i

_ERRORS = u"""
12:16: Invalid types for '==' (int *, Python object)
13:16: Invalid types for '==' (int, char *)
14:16: Invalid types for '==' (char *, int *)
23:16: 'likely' not a valid cython attribute or is being used incorrectly
23:16: 'likely' not a valid cython language construct
24:16: 'unlikely' not a valid cython attribute or is being used incorrectly
24:16: 'unlikely' not a valid cython language construct
25:19: 'likely' not a valid cython attribute or is being used incorrectly
25:19: 'likely' not a valid cython language construct
"""
