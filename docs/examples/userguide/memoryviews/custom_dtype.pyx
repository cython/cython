import numpy as np

CUSTOM_DTYPE = np.dtype([
    ('x', np.uint8),
    ('y', np.float32),
])

a = np.zeros(100, dtype=CUSTOM_DTYPE)

cdef packed struct custom_dtype_struct:
    # The struct needs to be packed since by default numpy dtypes aren't
    # aligned
    unsigned char x
    float y

def sum(custom_dtype_struct [:] a):

    cdef:
        unsigned char sum_x = 0
        float sum_y = 0.

    for i in range(a.shape[0]):
        sum_x += a[i].x
        sum_y += a[i].y

    return sum_x, sum_y
