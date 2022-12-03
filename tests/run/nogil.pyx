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

cdef double copy_array2() nogil:
    cdef double[4] x = [1.0, 3.0, 5.0, 7.0]
    cdef double[4] y
    y[:] = x[:]
    return y[0] + y[1] + y[2] + y[3]

cdef double copy_array3() nogil:
    cdef double[4] x = [2.0, 4.0, 6.0, 8.0]
    cdef double[4] y
    y = x
    return y[0] + y[1] + y[2] + y[3]

cdef void copy_array_exception(int n) nogil:
    cdef double[5] a = [1,2,3,4,5]
    cdef double[6] b
    b[:n] = a

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
    16.0
    """
    return copy_array2()

def test_copy_array3():
    """
    >>> test_copy_array3()
    20.0
    """
    return copy_array3()

def test_copy_array_exception(n):
    """
    >>> test_copy_array_exception(20)
    Traceback (most recent call last):
        ...
    ValueError: Assignment to slice of wrong length, expected 5, got 20
    """
    copy_array_exception(n)
    
def test_copy_array_exception_nogil(n): 
    """
    >>> test_copy_array_exception_nogil(20)
    Traceback (most recent call last):
        ...
    ValueError: Assignment to slice of wrong length, expected 5, got 20
    """
    with nogil:
        copy_array_exception(n)
