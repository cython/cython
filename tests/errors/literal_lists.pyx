def f():
    cdef int* p
    if False:
        p = [1, 2, 3]

_ERRORS = u"""
4:10: Literal list must be assigned to pointer at time of declaration
"""
