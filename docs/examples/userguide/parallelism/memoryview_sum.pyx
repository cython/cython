from cython.parallel import prange



cdef void func(double[:] x, double alpha) nogil:
    cdef Py_ssize_t i

    for i in prange(x.shape[0]):
        x[i] = alpha * x[i]
