# ticket: t183

cimport cython

@cython.cdivision(True)
cpdef cdiv_decorator(int a, int b):
    """
    >>> cdiv_decorator(-12, 5)
    -2
    """
    return a / b

@cython.cdivision(False)
cpdef pydiv_decorator(int a, int b):
    """
    >>> pydiv_decorator(-12, 5)
    -3
    """
    return a / b
