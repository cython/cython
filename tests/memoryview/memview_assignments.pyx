# mode: compile
# tag: memoryview

cdef double[::1] contig
# see if we can assign a strided value to a contiguous one
contig[:] = contig[::2]
