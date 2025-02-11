from cython.parallel import prange

i = cython.declare(cython.int)
n = cython.declare(cython.int, 30)
sum = cython.declare(cython.int, 0)

for i in prange(n, nogil=True):
    sum += i

print(sum)
