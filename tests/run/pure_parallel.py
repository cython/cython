# mode: run
# tag: openmp, pure3.6

import cython
from cython.parallel import prange, parallel


def prange_regression(n: cython.int, data: list):
    """
    >>> prange_regression(10, list(range(1, 4)))
    19
    """
    s: cython.int = 0
    i: cython.int
    d: cython.int[3] = data

    for i in prange(n, num_threads=3, nogil=True):
        s += d[i % 3]
    return s


def prange_with_gil(n: cython.int, x):
    """
    >>> sum(3*i for i in range(10))
    135
    >>> prange_with_gil(10, 3)
    135
    """
    i: cython.int
    s: cython.int = 0

    for i in prange(n, num_threads=3, nogil=True):
        with cython.gil:
            s += x * i

    return s


@cython.cfunc
def use_nogil(x, i: cython.int) -> cython.int:
    cx: cython.int = x
    with cython.nogil:
        return cx * i


def prange_with_gil_call_nogil(n: cython.int, x):
    """
    >>> sum(3*i for i in range(10))
    135
    >>> prange_with_gil(10, 3)
    135
    """
    i: cython.int
    s: cython.int = 0

    for i in prange(n, num_threads=3, nogil=True):
        with cython.gil:
            s += use_nogil(x, i)

    return s
