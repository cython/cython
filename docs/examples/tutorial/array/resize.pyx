from cpython cimport array
import array

cdef array.array a = array.array('i', [1, 2, 3])
cdef array.array b = array.array('i', [4, 5, 6])

# extend a with b, resize as needed
array.extend(a, b)
# resize a, leaving just original three elements
array.resize(a, len(a) - len(b))
