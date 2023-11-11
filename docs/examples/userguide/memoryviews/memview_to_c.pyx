cdef extern from "C_func_file.c":
    # C is include here so that it doesn't need to be compiled externally
    pass

cdef extern from "C_func_file.h":
    void multiply_by_10_in_C(double *, unsigned int)

import numpy as np

def multiply_by_10(arr):  # 'arr' is a one-dimensional numpy array

    if not arr.flags['C_CONTIGUOUS']:
        arr = np.ascontiguousarray(arr)  # Makes a contiguous copy of the numpy array.

    cdef double[::1] arr_memview = arr

    multiply_by_10_in_C(&arr_memview[0], arr_memview.shape[0])

    return arr


a = np.ones(5, dtype=np.double)
print(multiply_by_10(a))

b = np.ones(10, dtype=np.double)
b = b[::2]  # b is not contiguous.

print(multiply_by_10(b))  # but our function still works as expected.
