cimport numpy as cnp


def sum_of_squares(cnp.ndarray[double, ndim=1] arr):
    cdef long N = arr.shape[0]
    cdef double ss = 0
    for i in range(N):
        ss += arr[i]**2
    return ss
