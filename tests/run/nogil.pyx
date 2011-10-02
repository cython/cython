def test(int x):
    """
    >>> test(5)
    47
    >>> test(11)
    53
    """
    with nogil:
        f(x)
        x = g(x)
    return x

cdef void f(int x) nogil:
        cdef int y
        y = x + 42
        g(y)

cdef int g(int x) nogil:
        cdef int y
        y = x + 42
        return y

cdef int with_gil_func() except 0 with gil:
    raise Exception("error!")

cdef int nogil_func() nogil except 0:
    with_gil_func()

def test_nogil_exception_propagation():
    """
    >>> test_nogil_exception_propagation()
    Traceback (most recent call last):
       ...
    Exception: error!
    """
    with nogil:
        nogil_func()
