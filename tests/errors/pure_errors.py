# mode: error
# tag: warnings, werror

import cython

@cython.cfunc
@cython.locals(x=cython.int)
@cython.returns(cython.int)
def cdef_needs_gil(x):
    return x + 1


@cython.cfunc
@cython.nogil
@cython.locals(x=cython.int)
@cython.returns(cython.int)
def cdef_nogil(x):
    return x + 1


@cython.cfunc
@cython.nogil(True)
@cython.locals(x=cython.int)
@cython.returns(cython.int)
def cdef_nogil_true(x):
    return x + 1


@cython.cfunc
@cython.nogil(False)
@cython.locals(x=cython.int)
@cython.returns(cython.int)
def cdef_nogil_false(x):
    return x + 1


@cython.locals(x=cython.int)
def test_cdef_nogil(x):
    cdef_nogil(x)  # ok
    cdef_nogil_false(x)  # ok
    cdef_nogil_true(x)  # ok
    with cython.nogil:
        cdef_nogil_true(x)   # ok
        cdef_needs_gil(x)    # not ok
        cdef_nogil_false(x)  # not ok


def test_nested_gil_nogil(x: cython.int):
    arr: cython.int[5] = [1, 2, 3, 4, 5]
    with cython.nogil:
        with cython.nogil(False), cython.gil:
            cdef_nogil(x)  # ok
            cdef_needs_gil(x)  # ok
        with cython.gil(True), cython.nogil:
            cdef_nogil(x)  # ok
            cdef_needs_gil(x)  # not ok
        with cython.gil, cython.nogil, cython.wraparound(False):
            cdef_nogil(x)  # ok
            cdef_needs_gil(x)  # not ok
            x += arr[-1]  # not ok


@cython.nogil
def pyfunc(x):  # invalid
    return x + 1


@cython.exceptval(-1)
@cython.cfunc
def test_cdef_return_object_broken(x: object) -> object:
    return x


@cython.ccall
@cython.cfunc
def test_contradicting_decorators1(x: object) -> object:
    return x


@cython.cfunc
@cython.ccall
def test_contradicting_decorators2(x: object) -> object:
    return x


@cython.cfunc
@cython.ufunc
def add_one(x: cython.double) -> cython.double:
    return x+1


_ERRORS = """
30:0: Directive does not change previous value (nogil=False)
44:22: Calling gil-requiring function not allowed without gil
45:24: Calling gil-requiring function not allowed without gil
56:26: Calling gil-requiring function not allowed without gil
59:26: Calling gil-requiring function not allowed without gil
60:22: the result of using negative indices inside of code sections marked as 'wraparound=False' is undefined
63:0: Python functions cannot be declared 'nogil'
68:0: Exception clause not allowed for function returning Python object
74:0: cfunc and ccall directives cannot be combined
80:0: cfunc and ccall directives cannot be combined
86:0: Cannot apply @cfunc to @ufunc, please reverse the decorators.

# bugs:
74:0: 'test_contradicting_decorators1' redeclared
80:0: 'test_contradicting_decorators2' redeclared
"""
