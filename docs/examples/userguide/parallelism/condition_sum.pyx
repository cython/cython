from cython.parallel import prange

def psum(int n):

    cdef int i
    cdef int sum = 0

    for i in prange(n, nogil=True, use_threads_if=n>1000):
        sum += i

    return sum

psum(30)        # Executed sequentially
psum(10000)     # Executed in parallel
