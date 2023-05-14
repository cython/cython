from cython.parallel import prange
import cython
from cython.cimports.libc.math import sqrt

@cython.boundscheck(False)
@cython.wraparound(False)
def l2norm(x: cython.double[:]):
    total: cython.double = 0
    i: cython.Py_ssize_t
    for i in prange(x.shape[0], nogil=True):
        total += x[i]*x[i]
    return sqrt(total)
