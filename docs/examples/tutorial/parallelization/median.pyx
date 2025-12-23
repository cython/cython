# distutils: language = c++

from cython.parallel cimport parallel, prange
from libcpp.vector cimport vector
from libcpp.algorithm cimport nth_element
cimport cython
from cython.operator cimport dereference

import numpy as np

@cython.boundscheck(False)
@cython.wraparound(False)
def median_along_axis0(const double[:,:] x):
    cdef double[::1] out = np.empty(x.shape[1])
    cdef Py_ssize_t i, j

    cdef vector[double] *scratch
    cdef vector[double].iterator median_it
    with nogil, parallel():
        # allocate scratch space per loop
        scratch = new vector[double](x.shape[0])
        try:
            for i in prange(x.shape[1]):
                # copy row into scratch space
                for j in range(x.shape[0]):
                    dereference(scratch)[j] = x[j, i]
                median_it = scratch.begin() + scratch.size()//2
                nth_element(scratch.begin(), median_it, scratch.end())
                # for the sake of a simple example, don't handle even lengths...
                out[i] = dereference(median_it)
        finally:
            del scratch
    return np.asarray(out)

