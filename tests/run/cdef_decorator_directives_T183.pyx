__doc__ = u"""
    >>> cdiv_decorator(-12, 5)
    -2
    >>> pydiv_decorator(-12, 5)
    -3
"""

cimport cython

@cython.cdivision(True)
cpdef cdiv_decorator(int a, int b):
    return a / b

@cython.cdivision(False)
cpdef pydiv_decorator(int a, int b):
    return a / b
