from cython.parallel import prange

@cython.exceptval(-1)
@cython.cfunc
def func(n: cython.Py_ssize_t) -> cython.int:
    i: cython.Py_ssize_t

    for i in prange(n, nogil=True):
        if i == 8:
            with cython.gil:
                raise Exception()
        elif i == 4:
            break
        elif i == 2:
            return i
