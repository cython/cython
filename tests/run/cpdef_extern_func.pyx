# cython: c_string_type=str
# cython: c_string_encoding=ascii
# distutils: extra_compile_args=-fpermissive

__doc__ = """
>>> sqrt(1)
1.0
>>> pyx_sqrt(4)
2.0
>>> pxd_sqrt(9)
3.0
>>> log(10)  # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'log' is not defined
>>> strchr('abcabc', ord('c'))
'cabc'
>>> strchr(needle=ord('c'), haystack='abcabc')
'cabc'
"""

cdef extern from "math.h":
    cpdef double sqrt(double)
    cpdef double pyx_sqrt "sqrt"(double)
    cdef double log(double) # not wrapped

cdef extern from "string.h":
    # signature must be exact in C++, disagrees with C
    cpdef const char* strchr(const char *haystack, int needle);
