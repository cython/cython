# cython: profile=True
import cython

@cython.cfunc
@cython.inline
@cython.exceptval(-1.0)
def recip_square(i: cython.longlong) -> cython.double:
    return 1. / (i * i)

def approx_pi(n: cython.int = 10000000):
    val: cython.double = 0.
    k: cython.int
    for k in range(1, n + 1):
        val += recip_square(k)
    return (6 * val) ** .5
