# cython: profile=True

cimport cython




@cython.profile(False)
cdef inline double recip_square(long long i) except -1.0:
    return 1. / (i * i)

def approx_pi(int n=10000000):
    cdef double val = 0.
    cdef int k
    for k in range(1, n + 1):
        val += recip_square(k)
    return (6 * val) ** .5
