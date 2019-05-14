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

def div_double(np.ndarray[double, ndim=1] d):
    """
    >>> d = np.ndarray((2,))
    >>> d[0] = 1.0
    >>> d[1] = -1.0
    >>> div_double(d)
    [0.5, -0.5]
    """
    return d/2.0

def div_int(np.ndarray[int, ndim=1] d):
    """
    >>> d = np.ndarray((2,), dtype=np.int)
    >>> d[0] = 2
    >>> d[1] = -2
    >>> div_int(d)
    [1, -1]
    """
    return d//2
