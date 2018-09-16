from cython.parallel import prange

cdef int i
cdef int n = 30
cdef int sum = 0

for i in prange(n, nogil=True):
    sum += i

print(sum)
