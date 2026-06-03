# mode: run

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def test(int x):
    """
    >>> test(0)
    110
    """
    with nogil(True):
        x = f_nogil(x)
        with gil(True):
            x = f_gil(x)
    return x


cdef int f_nogil(int x) nogil:
    cdef int y
    y = x + 10
    return y


def f_gil(x):
    y = 0
    y = x + 100
    return y


cdef int with_gil_func() except? -1 with gil:
    raise Exception("error!")


cdef int nogil_func() except? -1 nogil:
    with_gil_func()


def test_nogil_exception_propagation():
    """
    >>> test_nogil_exception_propagation()
    Traceback (most recent call last):
       ...
    Exception: error!
    """
    with nogil:
        with gil:
            with nogil(True):
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


def test_nested():
    """
    >>> test_nested()
    240
    """
    cdef int res = 0

    with nogil(True):
        res = f_nogil(res)
        with gil(1 < 2):
            res = f_gil(res)
            with nogil:
                res = f_nogil(res)

        with gil:
            res = f_gil(res)
            with nogil(True):
                res = f_nogil(res)
            with nogil:
                res = f_nogil(res)

    return res


DEF FREE_GIL = True
DEF FREE_GIL_FALSE = False


def test_nested_condition_false():
    """
    >>> test_nested_condition_false()
    220
    """
    cdef int res = 0

    with gil(FREE_GIL_FALSE):
        res = f_gil(res)
        with nogil(False):
            res = f_gil(res)

        with nogil(FREE_GIL):
            res = f_nogil(res)
            with gil(False):
                res = f_nogil(res)

    return res

def test_try_finally():
    """
    >>> test_try_finally()
    113
    """
    cdef int res = 0

    try:
        with nogil(True):
            try:
                res = f_nogil(res)
                with gil(1 < 2):
                    try:
                        res = f_gil(res)
                    finally:
                        res += 1
            finally:
                res = res + 1
    finally:
        res += 1

    return res


ctypedef fused number_or_object:
    int
    float
    object


def test_fused(number_or_object x) -> number_or_object:
    """
    >>> test_fused[int](1)
    2
    >>> test_fused[float](1.0)
    2.0
    >>> test_fused[object](1)
    2
    >>> test_fused[object](1.0)
    2.0
    """
    cdef number_or_object res = x

    with nogil(number_or_object is not object):
        res = res + 1

    return res


ctypedef fused int_or_object:
    int
    object


def test_fused_object(int_or_object x):
    """
    >>> test_fused_object[object]("spam")
    456
    >>> test_fused_object[int](1000)
    1000
    """
    cdef int res = 0

    if int_or_object is object:
        with nogil(False):
            res += len(x)

        try:
            with nogil(int_or_object is object):
                try:
                    with gil(int_or_object is object):
                        res = f_gil(res)
                    with gil:
                        res = f_gil(res)
                    with gil(False):
                        res = f_nogil(res)

                    with gil(int_or_object is not object):
                        res = f_nogil(res)
                    with nogil(False):
                        res = f_nogil(res)

                    res = f_nogil(res)
                finally:
                    res = res + 1

            with nogil(int_or_object is not object):
                res = f_gil(res)

            with gil(int_or_object is not object):
                res = f_gil(res)

                with nogil(int_or_object is object):
                    res = f_nogil(res)

        finally:
            res += 1
    else:
        res = x

    return res


def test_fused_int(int_or_object x):
    """
    >>> test_fused_int[object]("spam")
    4
    >>> test_fused_int[int](1000)
    1452
    """
    cdef int res = 0

    if int_or_object is int:
        res += x

        try:
            with nogil(int_or_object is int):
                try:
                    with gil(int_or_object is int):
                        res = f_gil(res)
                    with gil:
                        res = f_gil(res)
                    with gil(False):
                        res = f_nogil(res)

                    with gil(int_or_object is not int):
                        res = f_nogil(res)
                    with nogil(False):
                        res = f_nogil(res)

                    res = f_nogil(res)
                finally:
                    res = res + 1

            with nogil(int_or_object is not int):
                res = f_gil(res)

            with gil(int_or_object is not int):
                res = f_gil(res)

                with nogil(int_or_object is int):
                    res = f_nogil(res)

        finally:
            res += 1
    else:
        with nogil(False):
            res = len(x)

    return res
