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


_ERRORS = """
44:22: Calling gil-requiring function not allowed without gil
45:24: Calling gil-requiring function not allowed without gil
49:0: Python functions cannot be declared 'nogil'
"""
