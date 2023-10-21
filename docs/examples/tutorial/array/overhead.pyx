from cpython cimport array
import array

cdef array.array a = array.array('i', [1, 2, 3])
cdef i32[:] ca = a

cdef i32 overhead(object a):
    cdef i32[:] ca = a
    return ca[0]

cdef i32 no_overhead(i32[:] ca):
    return ca[0]

print(overhead(a))  # new memory view will be constructed, overhead
print(no_overhead(ca))  # ca is already a memory view, so no overhead
