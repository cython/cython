__doc__ = u"""
    >>> single_py(1, 2)
    True
    >>> single_py(2, 1)
    False
    >>> cascaded_py(1, 2, 3)
    True
    >>> cascaded_py(1, 2, -1)
    False
    >>> cascaded_py(10, 2, 3)
    False

    >>> single_c(1, 2)
    True
    >>> single_c(2, 1)
    False
    >>> cascaded_c(1, 2, 3)
    True
    >>> cascaded_c(1, 2, -1)
    False
    >>> cascaded_c(10, 2, 3)
    False
"""

def single_py(a, b):
    return a < b

def cascaded_py(a, b, c):
    return a < b < c

def single_c(int a, int b):
    return a < b

def cascaded_c(double a, double b, double c):
    return a < b < c
