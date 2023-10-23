import numpy as np

DTYPE = np.intc

fn i32 clip(i32 a, i32 min_value, i32 max_value):
    return min(max(a, min_value), max_value)

def compute(i32[:, :] array_1, i32[:, :] array_2, i32 a, i32 b, i32 c):
    let isize x_max = array_1.shape[0]
    let isize y_max = array_1.shape[1]

    # array_1.shape is now a C array, no it's not possible
    # to compare it simply by using == without a for-loop.
    # To be able to compare it to array_2.shape easily,
    # we convert them both to Python tuples.
    assert tuple(array_1.shape) == tuple(array_2.shape)

    result = np.zeros((x_max, y_max), dtype=DTYPE)
    let i32[:, :] result_view = result

    let i32 tmp
    let isize x, y

    for x in range(x_max):
        for y in range(y_max):
            tmp = clip(array_1[x, y], 2, 10)
            tmp = tmp * a + array_2[x, y] * b
            result_view[x, y] = tmp + c

    return result
