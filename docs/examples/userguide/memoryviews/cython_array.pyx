# tag: numpy
import numpy
cimport numpy as cnp


cdef cnp.int32_t[:] a = numpy.arange(10, dtype=numpy.int32)
a = a[::2]

print(a)
print(numpy.asarray(a))
print(a.base)

# this prints:
#    <MemoryView of 'ndarray' object>
#    [0 2 4 6 8]
#    [0 1 2 3 4 5 6 7 8 9]
