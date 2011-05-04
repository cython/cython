# mode: error

cimport cython.parallel.parallel as p
from cython.parallel cimport something

import cython.parallel.parallel as p
from cython.parallel import something

from cython.parallel cimport prange

import cython.parallel

prange(1, 2, 3, schedule='dynamic')

cdef int i

with nogil, cython.parallel.parallel():
    for i in prange(10, schedule='invalid_schedule'):
        pass

with cython.parallel.parallel():
    print "hello world!"

cdef int *x = NULL

with nogil, cython.parallel.parallel():
    for j in prange(10):
        pass

    for x[1] in prange(10):
        pass

    for x in prange(10):
        pass

    with cython.parallel.parallel():
        pass

with nogil, cython.parallel.parallel:
    pass

_ERRORS = u"""
e_cython_parallel.pyx:3:8: cython.parallel.parallel is not a module
e_cython_parallel.pyx:4:0: No such directive: cython.parallel.something
e_cython_parallel.pyx:6:7: cython.parallel.parallel is not a module
e_cython_parallel.pyx:7:0: No such directive: cython.parallel.something
e_cython_parallel.pyx:13:6: prange() can only be used as part of a for loop
e_cython_parallel.pyx:13:6: prange() can only be used without the GIL
e_cython_parallel.pyx:18:19: Invalid schedule argument to prange: invalid_schedule
c_cython_parallel.pyx:21:29: The parallel section may only be used without the GIL
e_cython_parallel.pyx:27:10: target may not be a Python object as we don't have the GIL
e_cython_parallel.pyx:30:9: Can only iterate over an iteration variable
e_cython_parallel.pyx:33:10: Must be of numeric type, not int *
e_cython_parallel.pyx:36:33: Closely nested 'with parallel:' blocks are disallowed
e_cython_parallel.pyx:39:12: The parallel directive must be called
"""
