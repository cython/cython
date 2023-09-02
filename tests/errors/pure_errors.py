# mode: error
# tag: warnings

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
44:22: Calling gil-requiring function not allowed without gil
45:24: Calling gil-requiring function not allowed without gil
48:0: Python functions cannot be declared 'nogil'
53:0: Exception clause not allowed for function returning Python object
59:0: cfunc and ccall directives cannot be combined
65:0: cfunc and ccall directives cannot be combined
71:0: Cannot apply @cfunc to @ufunc, please reverse the decorators.
"""

_WARNINGS = """
30:0: Directive does not change previous value (nogil=False)
# bugs:
59:0: 'test_contradicting_decorators1' redeclared
65:0: 'test_contradicting_decorators2' redeclared
"""
