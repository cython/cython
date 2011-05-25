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

cdef int y

for i in prange(10, nogil=True):
    i = y * 4
    y = i

for i in prange(10, nogil=True):
    y = i
    i = y * 4
    y = i


with nogil, cython.parallel.parallel():
    i = y
    y = i

for i in prange(10, nogil=True):
    y += i
    y *= i

with nogil, cython.parallel.parallel("invalid"):
    pass

with nogil, cython.parallel.parallel(invalid=True):
    pass

def f(x):
    cdef int i

    with nogil, cython.parallel.parallel():
        with gil:
            yield x

        for i in prange(10):
            with gil:
                yield x

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
e_cython_parallel.pyx:36:33: Closely nested parallel with blocks are disallowed
e_cython_parallel.pyx:39:12: The parallel directive must be called
e_cython_parallel.pyx:45:10: Expression value depends on previous loop iteration, cannot execute in parallel
e_cython_parallel.pyx:55:9: Expression depends on an uninitialized thread-private variable
e_cython_parallel.pyx:60:6: Reduction operator '*' is inconsistent with previous reduction operator '+'
e_cython_parallel.pyx:62:36: cython.parallel.parallel() does not take positional arguments
e_cython_parallel.pyx:65:36: Invalid keyword argument: invalid
e_cython_parallel.pyx:73:12: Yield not allowed in parallel sections
e_cython_parallel.pyx:77:16: Yield not allowed in parallel sections
"""
