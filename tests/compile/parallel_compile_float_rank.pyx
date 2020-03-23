# mode: compile

from cython.parallel import *

cdef ssize_t i
cdef double[:,::1] X
cdef int j, k

with nogil, parallel():
   for i in range(10):
       pass

# simple device offload
with nogil, parallel(device={}):
    for i in prange(4):
        pass

# annotated device offload enbedded in context in gil mode
with device({X:'from', j:'to', k:'tofrom', i:'alloc'}):
    j = 0
    with nogil, parallel(device={X:'from'}):
        for i in prange(4):
            pass
