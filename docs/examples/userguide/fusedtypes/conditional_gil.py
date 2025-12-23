import cython

double_or_object = cython.fused_type(cython.double, object)

def increment(x: double_or_object):
    with cython.nogil(double_or_object is not object):
        # Same code handles both cython.double (GIL is released)
        # and python object (GIL is not released).
        x = x + 1
    return x

increment(5.0)  # GIL is released during increment
increment(5)    # GIL is acquired during increment
