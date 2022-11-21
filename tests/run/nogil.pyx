# mode: run

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


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

cdef void release_gil_in_nogil() nogil:
    # This should generate valid code with/without the GIL
    with nogil:
        pass

cpdef void release_gil_in_nogil2() nogil:
    # This should generate valid code with/without the GIL
    with nogil:
        pass

def test_release_gil_in_nogil():
    """
    >>> test_release_gil_in_nogil()
    """
    with nogil:
        release_gil_in_nogil()
    with nogil:
        release_gil_in_nogil2()
    release_gil_in_nogil()
    release_gil_in_nogil2()

cdef void get_gil_in_nogil() nogil:
    with gil:
        pass

cpdef void get_gil_in_nogil2() nogil:
    with gil:
        pass

def test_get_gil_in_nogil():
    """
    >>> test_get_gil_in_nogil()
    """
    with nogil:
        get_gil_in_nogil()
    with nogil:
        get_gil_in_nogil2()
    get_gil_in_nogil()
    get_gil_in_nogil2()

cdef int with_gil_func() except -1 with gil:
    raise Exception("error!")

cdef int nogil_func() except -1 nogil:
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


cdef int write_unraisable() noexcept nogil:
    with gil:
        raise ValueError()


def test_unraisable():
    """
    >>> print(test_unraisable())  # doctest: +ELLIPSIS
    ValueError
    Exception...ignored...
    """
    import sys
    old_stderr = sys.stderr
    stderr = sys.stderr = StringIO()
    try:
        write_unraisable()
    finally:
        sys.stderr = old_stderr
    return stderr.getvalue().strip()


cdef int initialize_array() nogil:
    cdef int[4] a = [1, 2, 3, 4]
    return a[0] + a[1] + a[2] + a[3]

cdef int copy_array() nogil:
    cdef int[4] a
    a[:] = [0, 1, 2, 3]
    return a[0] + a[1] + a[2] + a[3]

cdef void copy_array2() nogil:
    cdef double[16] x
    cdef double[16] y
    y[:] = x[:]
    y = x

def test_initalize_array():
    """
    >>> test_initalize_array()
    10
    """
    return initialize_array()

def test_copy_array():
    """
    >>> test_copy_array()
    6
    """
    return copy_array()

def test_copy_array2():
    """
    >>> test_copy_array2()
    """
    return copy_array2()
