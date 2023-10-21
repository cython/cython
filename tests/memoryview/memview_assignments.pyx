# mode: compile
# tag: memoryview

cdef f64[::1] contig
# see if we can assign a strided value to a contiguous one
contig[:] = contig[::2]
