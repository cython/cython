# cython: profile=True
import cython

def recip_square(i: cython.longlong):
    return 1. / i ** 2

def approx_pi(n: cython.int = 10000000):
    val: cython.double = 0.
    k: cython.int
    for k in range(1, n + 1):
        val += recip_square(k)
    return (6 * val) ** .5
