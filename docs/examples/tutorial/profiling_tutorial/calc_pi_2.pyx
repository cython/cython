# cython: profile=True

def recip_square(i32 i):
    return 1. / i ** 2

def approx_pi(i32 n=10000000):
    cdef f64 val = 0.
    cdef i32 k
    for k in range(1, n + 1):
        val += recip_square(k)
    return (6 * val) ** .5
