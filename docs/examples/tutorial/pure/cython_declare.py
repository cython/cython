import cython

x = cython.declare(cython.int)              # cdef int x
y = cython.declare(cython.double, 0.57721)  # cdef double y = 0.57721
