# mode: error
# tag: pxd

# OK

cdef int wider_exception_check(int x, int y) except 0:
    return 2

cdef int no_exception_raised(int x, int y):
    return 2

cdef int any_exception_value1(int x, int y) except *:
    return 2

cdef int any_exception_value2(int x, int y) except -1:
    return 2

cdef int any_exception_value3(int x, int y) except -2:
    return 2

cdef int any_exception_value4(int x, int y) except? -2:
    return 2

cdef int optimised_exception_value(int x, int y) except *:  # => except? -1
    return 2


# NOK

cdef int wrong_args(int x, int y):
    return 2

cdef int wrong_return_type(int x, int y):
    return 2

cdef int foreign_exception_value(int x, int y):
    return 2

cdef int narrower_exception_check(int x, int y) except? 0:
    return 2

cdef int wrong_exception_value(int x, int y) except 1:
    return 2

cdef int wrong_exception_value_check(int x, int y) except? 1:
    return 2

cdef int wrong_exception_value_optimised_check(int x, int y) except *:
    return 2

cdef int wrong_exception_value_optimised(int x, int y) except *:
    return 2

cdef int narrower_exception_check_optimised(int x, int y) except *:
    return 2


_ERRORS = """
30:5: Function signature does not match previous declaration
33:5: Function signature does not match previous declaration
36:5: Function signature does not match previous declaration
39:5: Function signature does not match previous declaration
42:5: Function signature does not match previous declaration
45:5: Function signature does not match previous declaration
48:5: Function signature does not match previous declaration
51:5: Function signature does not match previous declaration
54:5: Function signature does not match previous declaration
"""
