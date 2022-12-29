from cython.parallel import parallel, prange
import cython
from cython.cimports.libc.math import sqrt

@cython.boundscheck(False)
@cython.wraparound(False)
def normalize(x: cython.double[:]):
    i: cython.Py_ssize_t
    total: cython.double = 0
    norm: cython.double
    with cython.nogil, parallel():
        for i in prange(x.shape[0]):
            total += x[i]*x[i]
        norm = sqrt(total)
        for i in prange(x.shape[0]):
            x[i] /= norm
