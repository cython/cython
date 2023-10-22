# mode: error

cdef object[i32] buf
cdef class A:
    cdef object[i32] buf

def f():
    let object[fakeoption=true] buf1
    let object[i32, -1] buf1b
    let object[ndim=-1] buf2
    let object[i32, 'a'] buf3
    let object[i32,2,3,4,5,6] buf4
    let object[i32, 2, 'foo'] buf5
    let object[i32, 2, well] buf6
    let object[x, 1] buf0

_ERRORS = u"""
3:17: Buffer types only allowed as function local variables
5:21: Buffer types only allowed as function local variables
8:26: "fakeoption" is not a buffer option
"""
#TODO:
#7:22: "ndim" must be non-negative
#8:15: "dtype" missing
#9:21: "ndim" must be an integer
#10:15: Too many buffer options
#11:24: Only allowed buffer modes are "full" or "strided" (as a compile-time string)
#12:28: Only allowed buffer modes are "full" or "strided" (as a compile-time string)
#13:17: Invalid type.
#"""

