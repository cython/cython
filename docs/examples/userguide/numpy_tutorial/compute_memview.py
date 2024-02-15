import numpy as np
import cython

DTYPE = np.intc

@cython.cfunc
def clip(a: cython.int, min_value: cython.int, max_value: cython.int) -> cython.int:
    return min(max(a, min_value), max_value)


def compute(array_1: cython.int[:, :], array_2: cython.int[:, :],
        a: cython.int, b: cython.int, c: cython.int):

    x_max: cython.Py_ssize_t = array_1.shape[0]
    y_max: cython.Py_ssize_t = array_1.shape[1]

    # array_1.shape is now a C array, no it's not possible
    # to compare it simply by using == without a for-loop.
    # To be able to compare it to array_2.shape easily,
    # we convert them both to Python tuples.
    assert tuple(array_1.shape) == tuple(array_2.shape)

    result = np.zeros((x_max, y_max), dtype=DTYPE)
    result_view: cython.int[:, :] = result

    tmp: cython.int
    x: cython.Py_ssize_t
    y: cython.Py_ssize_t

    for x in range(x_max):
        for y in range(y_max):

            tmp = clip(array_1[x, y], 2, 10)
            tmp = tmp * a + array_2[x, y] * b
            result_view[x, y] = tmp + c

    return result
