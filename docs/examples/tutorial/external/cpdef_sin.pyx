"""
>>> sin(0)
0.0
"""

cdef extern from "math.h":
    cpdef double sin(double x)
