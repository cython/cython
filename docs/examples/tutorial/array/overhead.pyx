from cpython cimport array
import array

cdef array.array a = array.array('i', [1, 2, 3])
cdef int[:] ca = a


cdef int overhead(object a):
    cdef int[:] ca = a
    return ca[0]


cdef int no_overhead(int[:] ca):
    return ca[0]

print(overhead(a))  # new memory view will be constructed, overhead
print(no_overhead(ca))  # ca is already a memory view, so no overhead
