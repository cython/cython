# cython: remove_unreachable=False
# mode: error

cdef int f_nogil(int x) nogil:
    cdef int y
    y = x + 10
    return y


def f_gil(x):
    y = 0
    y = x + 100
    return y


def illegal_gil_usage():
    cdef int res = 0
    with nogil(True):
        res = f_gil(res)

        with nogil(True):
            res = f_gil(res)

        with gil(False):
            res = f_gil(res)

    with nogil(False):
        res = f_nogil(res)


def foo(a):
    return a < 10


def non_constant_condition(int x) -> int:
    cdef int res = x
    with nogil(x < 10):
        res = f_nogil(res)

    with gil(foo(x)):
         res = f_gil(res)


ctypedef fused number_or_object:
    float
    object


def fused_type(number_or_object x):
    with nogil(number_or_object is object):
        res = x + 1

    # This should be fine
    with nogil(number_or_object is float):
        res = x + 1

    return res


_ERRORS = u"""
19:14: Accessing Python global or builtin not allowed without gil
19:19: Calling gil-requiring function not allowed without gil
19:19: Coercion from Python not allowed without the GIL
19:19: Constructing Python tuple not allowed without gil
19:20: Converting to Python object not allowed without gil
21:13: Trying to release the GIL while it was previously released.
22:18: Accessing Python global or builtin not allowed without gil
22:23: Calling gil-requiring function not allowed without gil
22:23: Coercion from Python not allowed without the GIL
22:23: Constructing Python tuple not allowed without gil
22:24: Converting to Python object not allowed without gil
25:18: Accessing Python global or builtin not allowed without gil
25:23: Calling gil-requiring function not allowed without gil
25:23: Coercion from Python not allowed without the GIL
25:23: Constructing Python tuple not allowed without gil
25:24: Converting to Python object not allowed without gil
37:17: Non-constant condition in a `with nogil(<condition>)` statement
40:16: Non-constant condition in a `with gil(<condition>)` statement
51:8: Assignment of Python object not allowed without gil
51:16: Calling gil-requiring function not allowed without gil
"""
