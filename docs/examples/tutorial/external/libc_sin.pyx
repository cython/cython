from libc.math cimport sin

cdef f64 f(f64 x):
    return sin(x * x)
