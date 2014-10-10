# mode: error
# tag: pxd

cdef int wrong_args(int x, int y):
    return 0

cdef int wrong_return_type(int x, int y):
    return 0

cdef int wrong_exception_check(int x, int y) except? 0:
    return 0

cdef int wrong_exception_value(int x, int y) except 1:
    return 0

cdef int wrong_exception_value_check(int x, int y) except? 1:
    return 0


_ERRORS = """
4:5: Function signature does not match previous declaration
7:5: Function signature does not match previous declaration
10:5: Function signature does not match previous declaration
13:5: Function signature does not match previous declaration
16:5: Function signature does not match previous declaration
"""
