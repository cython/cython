# mode: error

from cython.parallel cimport parallel, prange

cdef int i

# valid
with nogil, parallel(num_threads=None):
    pass

# invalid
with nogil, parallel(num_threads=None, num_threads=None):
    pass

with nogil, parallel(num_threads=0):
    pass

with nogil, parallel(num_threads=i):
    pass

with nogil, parallel(num_threads=2, num_threads=2):
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
12:20: Duplicate keyword argument found: num_threads
15:20: argument to num_threads must be greater than 0
21:20: Duplicate keyword argument found: num_threads
25:19: num_threads already declared in outer section
29:19: num_threads must be declared in the parent parallel section
"""
