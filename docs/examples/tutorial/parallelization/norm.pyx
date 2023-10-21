from cython.parallel cimport prange
cimport cython
from libc.math cimport sqrt

@cython.boundscheck(false)
@cython.wraparound(false)
def l2norm(f64[:] x):
    cdef f64 total = 0
    cdef usize i
    for i in prange(x.shape[0], nogil=true):
        total += x[i] * x[i]
    return sqrt(total)
