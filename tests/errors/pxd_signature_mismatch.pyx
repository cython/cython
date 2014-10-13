# mode: error
# tag: pxd

cdef int wrong_args(int x, int y):
    return 2

cdef int wrong_return_type(int x, int y):
    return 2

cdef int wrong_exception_check(int x, int y) except? 0:
    return 2

cdef int wrong_exception_value(int x, int y) except 1:
    return 2

cdef int wrong_exception_value_check(int x, int y) except? 1:
    return 2

cdef int inherit_exception_value(int x, int y):
    return 2

cdef int inherit_exception_check(int x, int y):
    return 2


_ERRORS = """
4:5: Function signature does not match previous declaration
7:5: Function signature does not match previous declaration
10:5: Function signature does not match previous declaration
13:5: Function signature does not match previous declaration
16:5: Function signature does not match previous declaration
19:5: Function signature does not match previous declaration
22:5: Function signature does not match previous declaration
"""
