# mode: run
# tag: pythran, numpy, cpp
# cython: np_pythran=True

import numpy as np
cimport numpy as cnp

def diffuse():
    """
    >>> u = diffuse()
    >>> count_non_zero = np.sum(u > 0)
    >>> 15000 < count_non_zero < (2**7) * (2**7) or count_non_zero
    True
    """
    lx, ly = (2**7, 2**7)
    u = np.zeros([lx, ly], dtype=np.double)
    u[lx // 2, ly // 2] = 1000.0
    _diffuse_numpy(u, 500)
    return u


def _diffuse_numpy(cnp.ndarray[double, ndim=2] u, int N):
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


def calculate_tax(cnp.ndarray[double, ndim=1] d):
    """
    >>> mu, sigma = 10.64, .35
    >>> np.random.seed(1234)
    >>> d = np.random.lognormal(mu, sigma, 10000)
    >>> avg = calculate_tax(d)
    >>> 0.243 < avg < 0.244 or avg  # 0.24342652180085891
    True
    """
    tax_seg1 = d[(d > 256303)] * 0.45 - 16164.53
    tax_seg2 = d[(d > 54057) & (d <= 256303)] * 0.42 - 8475.44
    seg3 = d[(d > 13769) & (d <= 54057)] - 13769
    seg4 = d[(d > 8820) & (d <= 13769)] - 8820
    prog_seg3 = seg3 * 0.0000022376 + 0.2397
    prog_seg4 = seg4 * 0.0000100727 + 0.14
    return (
        np.sum(tax_seg1) +
        np.sum(tax_seg2) +
        np.sum(seg3 * prog_seg3 + 939.57) +
        np.sum(seg4 * prog_seg4)
    ) / np.sum(d)
