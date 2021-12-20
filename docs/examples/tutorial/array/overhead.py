import cython
from cython.cimports.cpython import array
import array

a = cython.declare(array.array)
ca = cython.declare(cython.int[:])
a = array.array('i', [1, 2, 3])
ca = a

@cython.cfunc
def overhead(a: object) -> cython.int:
    ca: cython.int[:] = a
    return ca[0]

@cython.cfunc
def no_overhead(ca: cython.int[:]) -> cython.int:
    return ca[0]

print(overhead(a))  # new memory view will be constructed, overhead
print(no_overhead(ca))  # ca is already a memory view, so no overhead
