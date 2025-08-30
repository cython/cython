# tag: openmp

# distutils: extra_compile_args=-fopenmp
# distutils: extra_link_args=-fopenmp

import numpy as np
import cython
from cython.parallel import prange

my_type = cython.fused_type(cython.int, cython.double, cython.longlong)


# We declare our plain c function nogil
@cython.exceptval(check=False)
@cython.nogil
@cython.cfunc
def clip(a: my_type, min_value: my_type, max_value: my_type) -> my_type:
    return min(max(a, min_value), max_value)


@cython.boundscheck(False)
@cython.wraparound(False)
def compute(array_1: my_type[:, ::1], array_2: my_type[:, ::1], a: my_type, b: my_type, c: my_type):

    x_max: cython.Py_ssize_t = array_1.shape[0]
    y_max: cython.Py_ssize_t = array_1.shape[1]

    assert tuple(array_1.shape) == tuple(array_2.shape)

    if my_type is cython.int:
        dtype = np.intc
    elif my_type is cython.double:
        dtype = np.double
    elif my_type is cython.longlong:
        dtype = np.longlong

    result = np.zeros((x_max, y_max), dtype=dtype)
    result_view: my_type[:, ::1] = result

    tmp: my_type
    x: cython.Py_ssize_t
    y: cython.Py_ssize_t

    # We use prange here.
    for x in prange(x_max, nogil=True):
        for y in range(y_max):

            tmp = clip(array_1[x, y], 2, 10)
            tmp = tmp * a + array_2[x, y] * b
            result_view[x, y] = tmp + c

    return result
