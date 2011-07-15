# mode: error

from cython.parallel cimport prange

def invalid_closure_reduction():
    sum = 0
    def inner():
        nonlocal sum
        cdef int i
        for i in prange(10, nogil=True):
            with gil:
                sum += i

_ERRORS = u"""
e_cython_parallel_pyobject_reduction.pyx:10:23: Python objects cannot be reductions
"""
