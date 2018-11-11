# mode: run
# tag: pythran, numpy, cpp
# cython: np_pythran=True

import numpy as np
cimport numpy as np

def trigo(np.ndarray[double, ndim=1] angles):

    """
    >>> a = np.array([0., np.pi, np.pi *2])
    >>> trigo(a)
    array([ 1., -1.,  1.])
    """
    return np.cos(angles)

def power(np.ndarray[double, ndim=1] values):

    """
    >>> a = np.array([0., 1., 2.])
    >>> res = power(a)
    >>> res[0], res[1], res[2]
    (0.0, 1.0, 8.0)
    """
    return values ** 3
