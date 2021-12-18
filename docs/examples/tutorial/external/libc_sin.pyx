from libc.math cimport sin


cdef double f(double x):
    return sin(x * x)
