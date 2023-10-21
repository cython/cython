# cython: infer_types=True
import numpy as np
cimport cython

DTYPE = np.intc

cdef i32 clip(i32 a, i32 min_value, i32 max_value):
    return min(max(a, min_value), max_value)

@cython.boundscheck(false)
@cython.wraparound(false)
def compute(i32[:, ::1] array_1, i32[:, ::1] array_2, i32 a, i32 b, i32 c):
    x_max = array_1.shape[0]
    y_max = array_1.shape[1]

    assert tuple(array_1.shape) == tuple(array_2.shape)

    result = np.zeros((x_max, y_max), dtype=DTYPE)
    cdef i32[:, ::1] result_view = result

    cdef i32 tmp
    cdef isize x, y

    for x in range(x_max):
        for y in range(y_max):
            tmp = clip(array_1[x, y], 2, 10)
            tmp = tmp * a + array_2[x, y] * b
            result_view[x, y] = tmp + c

    return result
