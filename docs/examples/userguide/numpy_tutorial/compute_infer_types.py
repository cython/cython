# cython: infer_types=True
import numpy as np
import cython

DTYPE = np.intc

@cython.cfunc
def clip(a: cython.int, min_value: cython.int, max_value: cython.int) -> cython.int:
    return min(max(a, min_value), max_value)


@cython.boundscheck(False)
@cython.wraparound(False)
def compute(array_1: cython.int[:, ::1], array_2: cython.int[:, ::1],
            a: cython.int, b: cython.int, c: cython.int):

    x_max = array_1.shape[0]
    y_max = array_1.shape[1]

    assert tuple(array_1.shape) == tuple(array_2.shape)

    result = np.zeros((x_max, y_max), dtype=DTYPE)
    result_view: cython.int[:, ::1] = result

    tmp: cython.int
    x: cython.Py_ssize_t
    y: cython.Py_ssize_t

    for x in range(x_max):
        for y in range(y_max):

            tmp = clip(array_1[x, y], 2, 10)
            tmp = tmp * a + array_2[x, y] * b
            result_view[x, y] = tmp + c

    return result
