# cython: remove_unreachable=False
# mode: error
import cython

@cython.nogil
@cython.cfunc
def f_nogil(x: cython.i32) -> cython.i32:
    y: cython.i32
    y = x + 10
    return y

def f_gil(x):
    y = 0
    y = x + 100
    return y

def illegal_gil_usage():
    res: cython.i32 = 0
    with cython.nogil(True):
        res = f_gil(res)

        with cython.nogil(True):
            res = f_gil(res)

    with cython.nogil(False):
        res = f_nogil(res)

def foo(a):
    return a < 10

def non_constant_condition(x: cython.i32) -> cython.i32:
    res: cython.i32 = x
    with cython.nogil(x < 10):
        res = f_nogil(res)

number_or_object = cython.fused_type(cython.f32, cython.object)

def fused_type(x: number_or_object):
    with cython.nogil(number_or_object is object):
        res = x + 1

    # This should be fine
    with cython.nogil(number_or_object is cython.f32):
        res = x + 1

    return res

def nogil_multiple_arguments(x: cython.i32) -> cython.i32:
    res: cython.i32 = x
    with cython.nogil(1, 2):
        res = f_nogil(res)

def nogil_keyworkd_arguments(x: cython.i32) -> cython.i32:
    res: cython.i32 = x
    with cython.nogil(kw=2):
        res = f_nogil(res)

@cython.gil(True)
@cython.cfunc
def wrong_decorator() -> cython.i32:
    return 0

_ERRORS = u"""
20:14: Accessing Python global or builtin not allowed without gil
20:19: Calling gil-requiring function not allowed without gil
20:19: Coercion from Python not allowed without the GIL
20:19: Constructing Python tuple not allowed without gil
20:20: Converting to Python object not allowed without gil
22:13: Trying to release the GIL while it was previously released.
23:18: Accessing Python global or builtin not allowed without gil
23:23: Calling gil-requiring function not allowed without gil
23:23: Coercion from Python not allowed without the GIL
23:23: Constructing Python tuple not allowed without gil
23:24: Converting to Python object not allowed without gil
33:24: Non-constant condition in a `with nogil(<condition>)` statement
40:8: Assignment of Python object not allowed without gil
40:16: Calling gil-requiring function not allowed without gil
50:9: Compiler directive nogil accepts one positional argument.
55:9: Compiler directive nogil accepts one positional argument.
58:0: The gil compiler directive is not allowed in function scope
"""
