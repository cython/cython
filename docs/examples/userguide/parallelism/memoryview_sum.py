from cython.parallel import prange

@cython.nogil
@cython.cfunc
def func(x: cython.double[:], alpha: cython.double) -> cython.void:
    i: cython.Py_ssize_t

    for i in prange(x.shape[0]):
        x[i] = alpha * x[i]
