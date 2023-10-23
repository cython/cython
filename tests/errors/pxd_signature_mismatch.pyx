# mode: error
# tag: pxd

# OK

fn int wider_exception_check(int x, int y) except 0:
    return 2

fn int no_exception_raised(int x, int y):
    return 2

fn int any_exception_value1(int x, int y) except *:
    return 2

fn int any_exception_value2(int x, int y) except -1:
    return 2

fn int any_exception_value3(int x, int y) except -2:
    return 2

fn int any_exception_value4(int x, int y) except? -2:
    return 2

fn int optimised_exception_value(int x, int y) except *:  # => except? -1
    return 2


# NOK

fn int wrong_args(int x, int y):
    return 2

fn int wrong_return_type(int x, int y):
    return 2

fn int foreign_exception_value(int x, int y):
    return 2

fn int narrower_exception_check(int x, int y) except? 0:
    return 2

fn int wrong_exception_value(int x, int y) except 1:
    return 2

fn int wrong_exception_value_check(int x, int y) except? 1:
    return 2

fn int wrong_exception_value_optimised_check(int x, int y) except *:
    return 2

fn int wrong_exception_value_optimised(int x, int y) except *:
    return 2

fn int narrower_exception_check_optimised(int x, int y) except *:
    return 2


_ERRORS = """
30:0: Function signature does not match previous declaration
33:0: Function signature does not match previous declaration
36:0: Function signature does not match previous declaration
39:0: Function signature does not match previous declaration
42:0: Function signature does not match previous declaration
45:0: Function signature does not match previous declaration
48:0: Function signature does not match previous declaration
51:0: Function signature does not match previous declaration
54:0: Function signature does not match previous declaration
"""
