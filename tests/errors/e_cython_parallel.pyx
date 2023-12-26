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

# Disabled nesting:

for i in prange(10, nogil=True):
    for y in prange(10):
        pass

with nogil, cython.parallel.parallel():
    for i in prange(10):
        for i in prange(10):
            pass


# Assign to private from parallel block in prange:
cdef int myprivate1, myprivate2

with nogil, cython.parallel.parallel():
    myprivate1 = 1
    for i in prange(10):
        myprivate1 = 3
        myprivate2 = 4
    myprivate2 = 2

# Disallow parallel with block reductions:
i = 0
with nogil, cython.parallel.parallel():
    i += 1

# Use of privates after the parallel with block
with nogil, cython.parallel.parallel():
    i = 1

print i
i = 2
print i

# Reading of reduction variables in the prange block
cdef int sum = 0
for i in prange(10, nogil=True):
    sum += i
    with gil:
        print sum

for pyobj in prange("hello"):
    pass

from cython import parallel
with nogil, parallel.parallel():
    for i in parallel.prange(10):
        pass

cdef int[:] dst, src = object()
for i in prange(10, nogil=True):
    dst = src

for i in prange(10, nogil=True, chunksize=20):
    pass

for i in prange(10, nogil=True, schedule='static', chunksize=-1):
    pass

for i in prange(10, nogil=True, schedule='runtime', chunksize=10):
    pass

cdef int chunksize():
    return 10

for i in prange(10, nogil=True, schedule='static', chunksize=chunksize()):
    pass

with nogil, cython.parallel.parallel():
    with cython.parallel.parallel():
        pass

cdef bint gil_function():
    return True

for i in prange(10, nogil=True, use_threads_if=gil_function()):
    pass

with nogil, parallel.parallel(use_threads_if=gil_function()):
    pass

def bar():

    python_var = object()

    cdef int i

    for i in prange(10, nogil=True, use_threads_if=python_var):
        pass

    with nogil, parallel.parallel(use_threads_if=python_var):
        pass

_ERRORS = u"""
3:8: cython.parallel.parallel is not a module
4:0: No such directive: cython.parallel.something
6:7: cython.parallel.parallel is not a module
7:0: No such directive: cython.parallel.something
13:6: prange() can only be used as part of a for loop
13:6: prange() can only be used without the GIL
18:19: Invalid schedule argument to prange: invalid_schedule
21:29: The parallel section may only be used without the GIL
27:8: target may not be a Python object as we don't have the GIL
30:9: Can only iterate over an iteration variable
33:8: Must be of numeric type, not int *
36:33: Nested parallel with blocks are disallowed
39:12: The parallel directive must be called
45:8: local variable 'y' referenced before assignment
55:8: local variable 'y' referenced before assignment
60:4: Reduction operator '*' is inconsistent with previous reduction operator '+'
62:36: cython.parallel.parallel() does not take positional arguments
65:36: Invalid keyword argument: invalid
73:12: 'yield' not allowed in parallel sections
77:16: 'yield' not allowed in parallel sections
97:8: Cannot assign to private of outer parallel block
98:8: Cannot assign to private of outer parallel block
104:4: Reductions not allowed for parallel blocks
110:6: local variable 'i' referenced before assignment
119:14: Cannot read reduction variable in loop body
121:19: prange() can only be used without the GIL
121:20: stop argument must be numeric
131:4: Memoryview slices can only be shared in parallel sections
133:42: Must provide schedule with chunksize
136:62: Chunksize must not be negative
139:62: Chunksize not valid for the schedule runtime
145:70: Calling gil-requiring function not allowed without gil
149:33: Nested parallel with blocks are disallowed
155:59: Calling gil-requiring function not allowed without gil
158:57: Calling gil-requiring function not allowed without gil
167:51: use_threads_if may not be a Python object as we don't have the GIL
170:49: use_threads_if may not be a Python object as we don't have the GIL
"""
