from cython.parallel import parallel, prange
from cython.cimports.libc.stdlib import abort, malloc, free

@cython.nogil
@cython.cfunc
def func(buf: cython.p_int) -> cython.void:
    pass
    # ...

idx = cython.declare(cython.Py_ssize_t)
i = cython.declare(cython.Py_ssize_t)
j = cython.declare(cython.Py_ssize_t)
n = cython.declare(cython.Py_ssize_t, 100)
local_buf = cython.declare(p_int)
size = cython.declare(cython.size_t, 10)

with cython.nogil, parallel():
    local_buf: cython.p_int = cython.cast(cython.p_int, malloc(cython.sizeof(cython.int) * size))
    if local_buf is cython.NULL:
        abort()

    # populate our local buffer in a sequential loop
    for i in range(size):
        local_buf[i] = i * 2

    # share the work using the thread-local buffer(s)
    for j in prange(n, schedule='guided'):
        func(local_buf)

    free(local_buf)
