# tag: numpy

cimport numpy as np

def divide(np.float64_t x, np.complex128_t y):
    """
    >>> divide(2, 1+1j)
    (1-1j)
    """
    return x / y

def pow(np.complex128_t x, np.complex128_t y):
    """
    >>> pow(1 + 1j, 2j)  # doctest: +ELLIPSIS
    (0.1599...+0.1328...j)
    """
    return x ** y
