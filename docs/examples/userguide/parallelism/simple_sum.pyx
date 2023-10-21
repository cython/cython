from cython.parallel import prange

cdef i32 i
cdef i32 n = 30
cdef i32 sum = 0

for i in prange(n, nogil=True):
    sum += i

print(sum)
