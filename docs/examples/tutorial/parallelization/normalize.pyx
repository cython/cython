from cython.parallel cimport parallel, prange
cimport cython
from libc.math cimport sqrt

@cython.boundscheck(false)
@cython.wraparound(false)
def normalize(f64[:] x):
    let isize i
    let f64 total = 0
    let f64 norm
    with nogil, parallel():
        for i in prange(x.shape[0]):
            total += x[i] * x[i]
        norm = sqrt(total)
        for i in prange(x.shape[0]):
            x[i] /= norm
