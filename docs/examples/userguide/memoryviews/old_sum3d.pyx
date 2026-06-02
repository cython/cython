cpdef int old_sum3d(object[int, ndim=3, mode='strided'] arr):
    cdef int I, J, K, total = 0
    I = arr.shape[0]
    J = arr.shape[1]
    K = arr.shape[2]
    for i in range(I):
        for j in range(J):
            for k in range(K):
                total += arr[i, j, k]
    return total
