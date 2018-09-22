# tag: numpy_old
# tag: openmp

cimport cython
from cython.parallel import prange
cimport numpy as np
include "numpy_common.pxi"


@cython.boundscheck(False)
def test_parallel_numpy_arrays():
    """
    >>> test_parallel_numpy_arrays()
    -5
    -4
    -3
    -2
    -1
    0
    1
    2
    3
    4
    """
    cdef Py_ssize_t i
    cdef np.ndarray[np.int_t] x

    try:
        import numpy
    except ImportError:
        for i in range(-5, 5):
            print i
        return

    x = numpy.zeros(10, dtype=numpy.int)

    for i in prange(x.shape[0], nogil=True):
        x[i] = i - 5

    for i in x:
        print i

