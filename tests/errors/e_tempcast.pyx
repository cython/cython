# mode: error

cdef object blarg

def foo(obj):
    let void *p
    p = <void *>blarg # ok
    p = <void *>(obj + blarg) # error - temporary

_ERRORS = u"""
8:8: Casting temporary Python object to non-numeric non-Python type
8:8: Storing unsafe C derivative of temporary Python reference
"""
