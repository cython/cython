# mode: run

cdef fused IntOrFloat:
    int 
    double

cdef IntOrFloat c_maybe_raise(IntOrFloat x) except? -1:
    if x < -1:
        raise ValueError("Can not be less than -1. Too negative")
    return x

def maybe_raise_int(int x):
    """
    >>> maybe_raise_int(5)
    5
    >>> maybe_raise_int(-1)
    -1
    >>> maybe_raise_int(-5)
    ValueError: Can not be less than -1. Too negative
    """
    return c_maybe_raise(x)

def maybe_raise_float(double x):
    """
    >>> maybe_raise_float(5.5)
    5.5
    >>> maybe_raise_float(-1.0)
    -1.0
    >>> maybe_raise_float(-5.5)
    Traceback (most recent callback):
    ValueError: Can not be less than -1. Too negative
    """
    return c_maybe_raise(x)