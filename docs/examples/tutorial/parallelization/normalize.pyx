from cython.parallel cimport parallel, prange
cimport cython
from libc.math cimport sqrt

@cython.boundscheck(False)
@cython.wraparound(False)
def normalize(double[:] x):
    cdef Py_ssize_t i
    cdef double total = 0
    cdef double norm
    with nogil, parallel():
        for i in prange(x.shape[0]):
            total += x[i]*x[i]
        norm = sqrt(total)
        for i in prange(x.shape[0]):
            x[i] /= norm

