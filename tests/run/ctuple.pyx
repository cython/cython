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

def indexing((int, double) xy):
    """
    >>> indexing((1, 2))
    (2, 3.0)
    """
    x = xy[0]
    y = xy[1]
    xy[0] = x + 1
    xy[1] = y + 1
    return xy

def unpacking((int, double) xy):
    """
    >>> unpacking((1, 2))
    (1, 2.0)
    """
    x, y = xy
    return x, y

cdef (int, double) side_effect((int, double) xy):
    print "called with", xy
    return xy

def unpacking_with_side_effect((int, double) xy):
    """
    >>> unpacking_with_side_effect((1, 2))
    called with (1, 2.0)
    (1, 2.0)
    """
    x, y = side_effect(xy)
    return x, y

def c_types(int a, double b):
    """
    >>> c_types(1, 2)
    (1, 2.0)
    """
    cdef int* a_ptr
    cdef double* b_ptr
    cdef (int*, double*) ab
    ab[0] = &a
    ab[1] = &b
    a_ptr, b_ptr = ab
    return a_ptr[0], b_ptr[0]

cpdef (int, double) ctuple_return_type(x, y):
    """
    >>> ctuple_return_type(1, 2)
    (1, 2.0)
    """
    return x, y
