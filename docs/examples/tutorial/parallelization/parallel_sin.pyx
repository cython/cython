from cython.parallel cimport prange
cimport cython
from libc.math cimport sin

import numpy as np

@cython.boundscheck(False)
@cython.wraparound(False)
def do_sine(double[:,:] input):
    cdef double[:,:] output = np.empty_like(input)
    cdef Py_ssize_t i, j

    for i in prange(input.shape[0], nogil=True):
        for j in range(input.shape[1]):
            output[i, j] = sin(input[i, j])
    return np.asarray(output)
