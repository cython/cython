cdef object[int] buf
cdef class A:
    cdef object[int] buf

def f():
    cdef object[fakeoption=True] buf1
    cdef object[int, -1] buf1b 
    cdef object[ndim=-1] buf2
    cdef object[int, 'a'] buf3
    cdef object[int,2,3,4,5,6] buf4

_ERRORS = u"""
1:11: Buffer types only allowed as function local variables
3:15: Buffer types only allowed as function local variables
6:27: "fakeoption" is not a buffer option
7:22: "ndim" must be non-negative
8:15: "dtype" missing
9:21: "ndim" must be an integer
10:15: Too many buffer options
"""

