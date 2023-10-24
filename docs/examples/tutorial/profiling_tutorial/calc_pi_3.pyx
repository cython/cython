# cython: profile=True

fn inline f64 recip_square(i128 i) except -1.0:
    return 1. / (i * i)

def approx_pi(i32 n=10000000):
    let f64 val = 0.
    let i32 k
    for k in range(1, n + 1):
        val += recip_square(k)
    return (6 * val) ** .5
