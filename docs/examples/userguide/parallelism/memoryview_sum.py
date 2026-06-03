from cython.parallel import prange

def func(x: cython.double[:], alpha: cython.double):
    i: cython.Py_ssize_t

    for i in prange(x.shape[0], nogil=True):
        x[i] = alpha * x[i]
