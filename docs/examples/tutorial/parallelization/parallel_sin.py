from cython.parallel import prange
import cython
from cython.cimports.libc.math import sin

import numpy as np

@cython.boundscheck(False)
@cython.wraparound(False)
def do_sine(input: cython.double[:,:]):
    output : cython.double[:,:] = np.empty_like(input)
    i : cython.Py_ssize_t
    j : cython.Py_ssize_t
    for i in prange(input.shape[0], nogil=True):
        for j in range(input.shape[1]):
            output[i, j] = sin(input[i, j])
    return np.asarray(output)
