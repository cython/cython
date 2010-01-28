cdef extern from "mymath.h":
    double sinc(double)

def call_sinc(x):
    return sinc(x)
