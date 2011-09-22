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

with nogil, parallel():
    for i in prange(10, num_threads=2):
        pass

# this one is valid
for i in prange(10, nogil=True, num_threads=2):
    pass

_ERRORS = u"""
e_invalid_num_threads.pyx:8:33: Coercion from Python not allowed without the GIL
e_invalid_num_threads.pyx:12:20: argument to num_threads must be greater than 0
e_invalid_num_threads.pyx:19:19: num_threads already declared in outer section
e_invalid_num_threads.pyx:23:19: num_threads must be declared in the parent parallel section
"""
