from cython.parallel import prange

cdef i32 i
cdef i32 n = 30
cdef i32 sum = 0

for i in prange(n, nogil=true):
    sum += i

print(sum)
