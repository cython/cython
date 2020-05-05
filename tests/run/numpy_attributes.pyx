# mode: run
# tag: numpy

import numpy as np
cimport numpy as cnp

cnp.import_array()

def access_shape():
    """
    >>> access_shape()
    10
    """
    cdef cnp.ndarray[double, ndim=2, mode='c'] array_in = \
                    1e10 * np.ones((10, 10))

    return array_in.shape[0]

def access_size():
    """
    >>> access_size()
    100
    """
    cdef cnp.ndarray[double, ndim=2, mode='c'] array_in = \
                    1e10 * np.ones((10, 10))

    return array_in.size

def access_strides():
    """
    >>> access_strides()
    (80, 8)
    """
    cdef cnp.ndarray[double, ndim=2, mode='c'] array_in = \
                    1e10 * np.ones((10, 10), dtype=np.float64)

    return (array_in.strides[0], array_in.strides[1])
