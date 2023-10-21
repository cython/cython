from cython.parallel cimport prange
cimport cython
from libc.math cimport sqrt

@cython.boundscheck(False)
@cython.wraparound(False)
def l2norm(f64[:] x):
    cdef f64 total = 0
    cdef usize i
    for i in prange(x.shape[0], nogil=True):
        total += x[i] * x[i]
    return sqrt(total)
