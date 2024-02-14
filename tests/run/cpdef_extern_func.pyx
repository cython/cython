# cython: c_string_type=str
# cython: c_string_encoding=ascii

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

>>> my_strchr('abcabc', ord('c'))
'cabc'
>>> my_strchr(needle=ord('c'), haystack='abcabc')
'cabc'

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
    """
    /* The return type of strchr differs between C and C++.
       This test is not interested in that, so create a wrapper function
       with a known return type.
    */
    static const char* my_strchr(const char *haystack, int needle) {
        return strchr(haystack, needle);
    }
    """
    cpdef const char* my_strchr(const char *haystack, int needle)
    cpdef const char* strchr "my_strchr" (const char *haystack, int needle)
