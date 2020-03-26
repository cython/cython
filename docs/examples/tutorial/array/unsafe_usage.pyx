from cpython cimport array
import array

cdef array.array a = array.array('i', [1, 2, 3])

# access underlying pointer:
print(a.data.as_ints[0])

from libc.string cimport memset

memset(a.data.as_voidptr, 0, len(a) * sizeof(int))
