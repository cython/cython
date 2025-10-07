# mode: run
# tag: perf_hints

from nogil_other cimport voidexceptnogil_in_other_pxd

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
    cdef int cn = n
    with nogil:
        copy_array_exception(cn)

# Should still get a warning even though it's declared in a pxd
cdef void voidexceptnogil_in_pxd() nogil:
    pass

def test_performance_hint_nogil():
    """
    >>> test_performance_hint_nogil()
    """
    with nogil:
        voidexceptnogil_in_pxd()
        # The function call should generate a performance hint, but the definition should
        # not (since it's in an external pxd we don't control)
        voidexceptnogil_in_other_pxd()


cdef int f_in_pxd1() nogil except -1:
    return 0

cdef int f_in_pxd2() nogil:  # implicit except -1?
    return 0

def test_declared_in_pxd():
    """
    >>> test_declared_in_pxd()
    """
    with nogil:
        # no warnings here because we're in the same file as the declaration
        f_in_pxd1()
        f_in_pxd2()


# Note that we're only able to check the first line of the performance hint
_PERFORMANCE_HINTS = """
5:18: No exception value declared for 'f_in_pxd1' in pxd file.
6:18: No exception value declared for 'f_in_pxd2' in pxd file.
20:9: Exception check after calling 'f' will always require the GIL to be acquired.
24:0: Exception check on 'f' will always require the GIL to be acquired.
34:0: Exception check on 'release_gil_in_nogil' will always require the GIL to be acquired.
39:0: Exception check on 'release_gil_in_nogil2' will always require the GIL to be acquired.
49:28: Exception check after calling 'release_gil_in_nogil' will always require the GIL to be acquired.
51:29: Exception check after calling 'release_gil_in_nogil2' will always require the GIL to be acquired.
55:0: Exception check on 'get_gil_in_nogil' will always require the GIL to be acquired.
59:0: Exception check on 'get_gil_in_nogil2' will always require the GIL to be acquired.
68:24: Exception check after calling 'get_gil_in_nogil' will always require the GIL to be acquired.
70:25: Exception check after calling 'get_gil_in_nogil2' will always require the GIL to be acquired.
133:0: Exception check on 'copy_array_exception' will always require the GIL to be acquired.
184:28: Exception check after calling 'copy_array_exception' will always require the GIL to be acquired.
187:0: Exception check on 'voidexceptnogil_in_pxd' will always require the GIL to be acquired.
195:30: Exception check after calling 'voidexceptnogil_in_pxd' will always require the GIL to be acquired.
198:36: Exception check after calling 'voidexceptnogil_in_other_pxd' will always require the GIL to be acquired.
"""
