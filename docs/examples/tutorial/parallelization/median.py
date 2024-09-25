# distutils: language = c++

from cython.parallel import parallel, prange
from cython.cimports.libc.stdlib import malloc, free
from cython.cimports.libcpp.algorithm import nth_element
import cython
from cython.operator import dereference

import numpy as np

@cython.boundscheck(False)
@cython.wraparound(False)
def median_along_axis0(x: cython.double[:,:]):
    out: cython.double[::1] = np.empty(x.shape[1])
    i: cython.Py_ssize_t
    j: cython.Py_ssize_t
    scratch: cython.p_double
    median_it: cython.p_double
    with cython.nogil, parallel():
        # allocate scratch space per loop
        scratch = cython.cast(
            cython.p_double,
            malloc(cython.sizeof(cython.double)*x.shape[0]))
        try:
            for i in prange(x.shape[1]):
                # copy row into scratch space
                for j in range(x.shape[0]):
                    scratch[j] = x[j, i]
                median_it = scratch + x.shape[0]//2
                nth_element(scratch, median_it, scratch + x.shape[0])
                # for the sake of a simple example, don't handle even lengths...
                out[i] = dereference(median_it)
        finally:
            free(scratch)
    return np.asarray(out)
