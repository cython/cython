def convert(*o):
    """
    >>> convert(1, 2)
    (1, 2.0)

    >>> convert(1)
    Traceback (most recent call last):
    ...
    TypeError: Expected a tuple of size 2, got tuple
    >>> convert(1, 2, 3)
    Traceback (most recent call last):
    ...
    TypeError: Expected a tuple of size 2, got tuple
    """
    cdef (int, double) xy = o
    return xy

cpdef (int, double) ctuple_return_type(x, y):
    """
    >>> ctuple_return_type(1, 2)
    (1, 2.0)
    """
    return x, y
