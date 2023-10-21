"""
>>> sin(0)
0.0
"""

cdef extern from "math.h":
    cpdef f64 sin(f64 x)
