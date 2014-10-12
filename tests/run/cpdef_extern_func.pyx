# cython: c_string_type=str
# cython: c_string_encoding=ascii

__doc__ = """
>>> sqrt(1)
1.0
>>> pyx_sqrt(4)
2.0
>>> pxd_sqrt(9)
3.0
>>> log(10)
Traceback (most recent call last):
...
NameError: name 'log' is not defined

>>> strchr('abcabc', ord('c'))
'cabc'
"""

cdef extern from "math.h":
    cpdef double sqrt(double)
    cpdef double pyx_sqrt "sqrt"(double)
    cdef double log(double) # not wrapped

# cdef extern from "string.h":
#     cpdef char* strchr(const char *haystack, int needle);
