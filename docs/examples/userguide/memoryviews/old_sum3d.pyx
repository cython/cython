cpdef i32 old_sum3d(object[i32, ndim=3, mode='strided'] arr):
    let i32 I, J, K, total = 0
    I = arr.shape[0]
    J = arr.shape[1]
    K = arr.shape[2]
    for i in range(I):
        for j in range(J):
            for k in range(K):
                total += arr[i, j, k]
    return total
