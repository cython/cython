__doc__ = """
>>> sqrt(1)
1.0
>>> pyx_sqrt(4)
2.0
>>> pxd_sqrt(9)
3.0
>>> log(10)
Traceback (most recent call last):
NameError: name 'log' is not defined
"""

cdef extern from "math.h":
    cpdef double sqrt(double)
    cpdef double pyx_sqrt "sqrt"(double)
    cdef double log(double) # not wrapped
