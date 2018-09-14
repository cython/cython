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


@cython.locals(x=cython.int)
def test_cdef_nogil(x):
    cdef_nogil(x)  # ok
    with cython.nogil:
        cdef_needs_gil(x)  # not ok


@cython.nogil
def pyfunc(x):
    return x + 1


_ERRORS = """
25:22: Calling gil-requiring function not allowed without gil
29:0: Python functions cannot be declared 'nogil'
"""
