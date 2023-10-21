from cython.parallel cimport parallel, prange
cimport cython
from libc.math cimport sqrt

@cython.boundscheck(False)
@cython.wraparound(False)
def normalize(f64[:] x):
    cdef isize i
    cdef f64 total = 0
    cdef f64 norm
    with nogil, parallel():
        for i in prange(x.shape[0]):
            total += x[i] * x[i]
        norm = sqrt(total)
        for i in prange(x.shape[0]):
            x[i] /= norm
