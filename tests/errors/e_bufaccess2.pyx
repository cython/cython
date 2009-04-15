cimport e_bufaccess_pxd # was needed to provoke a bug involving ErrorType
import cython

def f():
    cdef object[e_bufaccess_pxd.T] buf

def withnogil_access_fail():
    cdef object[int] buf = None
    with nogil:
        buf[2] = 2

@cython.boundscheck(False)
def withnogil_access_ok():
    cdef object[int] buf = None
    with nogil:
        buf[2] = 2 # No error should be triggered here

@cython.boundscheck(False)
def withnogil_access_fail_2():
    cdef object[object] buf = None
    with nogil:
        buf[2] = 2 # Not OK as dtype is object

def withnogil_acquire(x):
    cdef object[int] buf
    with nogil:
        buf = x

_ERRORS = u"""
3:9: 'nothing' is not a type identifier
10:11: Cannot check buffer index bounds without gil; use boundscheck(False) directive
22:11: Cannot access buffer with object dtype without gil
22:11: Assignment of Python object not allowed without gil
27:12: Assignment of Python object not allowed without gil
"""
