from cython.parallel import prange

cdef i32 func(isize n) except -1:
    cdef isize i

    for i in prange(n, nogil=true):
        if i == 8:
            with gil:
                raise Exception()
        elif i == 4:
            break
        elif i == 2:
            return i
