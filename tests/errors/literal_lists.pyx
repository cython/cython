# mode: error

def f():
    cdef int* p
    if false():
        p = [1, 2, 3]

def false():
    return False

_ERRORS = u"""
6:8: Literal list must be assigned to pointer at time of declaration
"""
