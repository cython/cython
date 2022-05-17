from cython.cimports.cpython import array
import array

a = cython.declare(array.array, array.array('i', [1, 2, 3]))

# access underlying pointer:
print(a.data.as_ints[0])

from cython.cimports.libc.string import memset

memset(a.data.as_voidptr, 0, len(a) * cython.sizeof(cython.int))
