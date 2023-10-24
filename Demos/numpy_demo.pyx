cimport numpy as cnp

def sum_of_squares(cnp.ndarray[f64, ndim=1] arr):
    let i32 N = arr.shape[0]
    let f64 ss = 0
    for i in range(N):
        ss += arr[i] ** 2
    return ss
