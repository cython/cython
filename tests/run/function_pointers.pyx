cdef int square(int x) nogil:
    return x * x

cdef int call_func(int -> int f, int x) except? -1:
    if f == NULL:
        raise ValueError, "NULL function"
    return f(x)

cdef int -> int nogil square_ptr = square
cdef (int -> int, int) -> int except? -1 call_func_ptr = call_func

def call_square(int x):
    """
    >>> call_square(3)
    9
    """
    return call_func_ptr(square_ptr, x)

def call_null(int x):
    """
    >>> call_null(3)
    Traceback (most recent call last):
    ...
    ValueError: NULL function
    """
    return call_func_ptr(NULL, x)
