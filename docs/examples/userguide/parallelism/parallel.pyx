from cython.parallel import parallel, prange
from libc.stdlib cimport abort, malloc, free



cdef void func(int *buf) noexcept nogil:
    pass
    # ...

cdef Py_ssize_t idx, i, j, n = 100
cdef int * local_buf
cdef size_t size = 10




with nogil, parallel():
    local_buf = <int *> malloc(sizeof(int) * size)
    if local_buf is NULL:
        abort()

    # populate our local buffer in a sequential loop
    for i in range(size):
        local_buf[i] = i * 2

    # share the work using the thread-local buffer(s)
    for j in prange(n, schedule='guided'):
        func(local_buf)

    free(local_buf)
