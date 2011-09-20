# mode: error

from cython.parallel cimport parallel, prange

cdef int i

# valid
with nogil, parallel(num_threads=None):
    pass

# invalid
with nogil, parallel(num_threads=0):
    pass

with nogil, parallel(num_threads=i):
    pass

with nogil, parallel(num_threads=2):
    for i in prange(10, num_threads=2):
        pass

_ERRORS = u"""
e_invalid_num_threads.pyx:12:20: argument to num_threads must be greater than 0
e_invalid_num_threads.pyx:15:20: Invalid value for num_threads argument, expected an int
e_invalid_num_threads.pyx:19:19: num_threads already declared in outer section
"""
