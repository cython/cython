from cython.parallel import prange

def func(f64[:] x, f64 alpha):
    cdef isize i

    for i in prange(x.shape[0], nogil=true):
        x[i] = alpha * x[i]
