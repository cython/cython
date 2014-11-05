cdef int square(int x):
    return x * x

cdef int call_func(int -> int f, int x):
    return f(x)

cdef int -> int square_ptr = square
cdef (int -> int, int) -> int call_func_ptr = call_func

def call_square(int x):
    """
    >>> call_square(3)
    9
    """
    return call_func_ptr(square_ptr, x)
