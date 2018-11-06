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
