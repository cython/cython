# mode: run
# tag: pythran, numpy, cpp
# cython: np_pythran=True

import numpy as np
cimport numpy as cnp

def test():
    """
    >>> u = test()
    >>> count_non_zero = np.sum(u > 0)
    >>> 15000 < count_non_zero < (2**7) * (2**7) or count_non_zero
    True
    """
    lx, ly = (2**7, 2**7)
    u = np.zeros([lx, ly], dtype=np.double)
    u[lx // 2, ly // 2] = 1000.0
    diffuse_numpy(u, 500)
    return u


def diffuse_numpy(cnp.ndarray[double, ndim=2] u, int N):
    """
    Apply Numpy matrix for the Forward-Euler Approximation
    """
    cdef cnp.ndarray[double, ndim=2] temp = np.zeros_like(u)
    mu = 0.1

    for n in range(N):
        temp[1:-1, 1:-1] = u[1:-1, 1:-1] + mu * (
            u[2:, 1:-1] - 2 * u[1:-1, 1:-1] + u[0:-2, 1:-1] +
            u[1:-1, 2:] - 2 * u[1:-1, 1:-1] + u[1:-1, 0:-2])
        u[:, :] = temp[:, :]
        temp[:, :] = 0.0
