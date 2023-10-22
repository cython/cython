# cython: remove_unreachable=false
# mode: error

cdef i32 f_nogil(i32 x) nogil:
    let i32 y
    y = x + 10
    return y

def f_gil(x):
    y = 0
    y = x + 100
    return y

def illegal_gil_usage():
    let i32 res = 0
    with nogil(true):
        res = f_gil(res)

        with nogil(true):
            res = f_gil(res)

        with gil(false):
            res = f_gil(res)

    with nogil(false):
        res = f_nogil(res)

def foo(a):
    return a < 10

def non_constant_condition(int x) -> i32:
    let i32 res = x
    with nogil(x < 10):
        res = f_nogil(res)

    with gil(foo(x)):
         res = f_gil(res)

ctypedef fused number_or_object:
    f32
    object

def fused_type(number_or_object x):
    with nogil(number_or_object is object):
        res = x + 1

    # This should be fine
    with nogil(number_or_object is f32):
        res = x + 1

    return res


_ERRORS = u"""
17:14: Accessing Python global or builtin not allowed without gil
17:19: Calling gil-requiring function not allowed without gil
17:19: Coercion from Python not allowed without the GIL
17:19: Constructing Python tuple not allowed without gil
17:20: Converting to Python object not allowed without gil
19:13: Trying to release the GIL while it was previously released.
20:18: Accessing Python global or builtin not allowed without gil
20:23: Calling gil-requiring function not allowed without gil
20:23: Coercion from Python not allowed without the GIL
20:23: Constructing Python tuple not allowed without gil
20:24: Converting to Python object not allowed without gil
23:18: Accessing Python global or builtin not allowed without gil
23:23: Calling gil-requiring function not allowed without gil
23:23: Coercion from Python not allowed without the GIL
23:23: Constructing Python tuple not allowed without gil
23:24: Converting to Python object not allowed without gil
33:17: Non-constant condition in a `with nogil(<condition>)` statement
36:16: Non-constant condition in a `with gil(<condition>)` statement
45:8: Assignment of Python object not allowed without gil
45:16: Calling gil-requiring function not allowed without gil
"""
