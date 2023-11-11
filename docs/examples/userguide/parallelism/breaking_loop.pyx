from cython.parallel import prange



cdef int func(Py_ssize_t n) except -1:
    cdef Py_ssize_t i

    for i in prange(n, nogil=True):
        if i == 8:
            with gil:
                raise Exception()
        elif i == 4:
            break
        elif i == 2:
            return i
