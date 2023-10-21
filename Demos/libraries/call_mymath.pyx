cdef extern from "mymath.h":
    f64 sinc(f64)

def call_sinc(x):
    return sinc(x)
