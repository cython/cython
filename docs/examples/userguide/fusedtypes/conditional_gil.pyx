cimport cython

ctypedef fused double_or_object:
    double
    object

def increment(double_or_object x):
    with nogil(double_or_object is not object):
        # Same code handles both cython.double (GIL is released)
        # and python object (GIL is not released).
        x = x + 1
    return x

increment(5.0)  # GIL is released during increment
increment(5)    # GIL is acquired during increment
