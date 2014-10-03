def simple_convert(*o):
    """
    >>> simple_convert(1, 2)
    (1, 2.0)

    >>> simple_convert(1)
    Traceback (most recent call last):
    ...
    TypeError: Expected a tuple of size 2, got tuple
    >>> simple_convert(1, 2, 3)
    Traceback (most recent call last):
    ...
    TypeError: Expected a tuple of size 2, got tuple
    """
    cdef (int, double) xy = o
    return xy

def rotate_via_indexing((int, int, double) xyz):
    """
    >>> rotate_via_indexing((1, 2, 3))
    (2, 3, 1.0)
    """
    a = xyz[0]
    xyz[0] = xyz[1]
    xyz[1] = <int>xyz[2]
    xyz[-1] = a
    return xyz

cpdef (int, double) ctuple_return_type(x, y):
    """
    >>> ctuple_return_type(1, 2)
    (1, 2.0)
    """
    return x, y
