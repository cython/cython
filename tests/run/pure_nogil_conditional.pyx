# mode: run
# tag: pure, nogil

import cython

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def test(x: cython.int):
    """
    >>> test(0)
    110
    """
    with cython.nogil(True):
        x = f_nogil(x)
        with cython.gil(True):
            x = f_gil(x)
    return x


@cython.nogil
@cython.cfunc
def f_nogil(x: cython.int) -> cython.int:
    y: cython.int
    y = x + 10
    return y


def f_gil(x):
    y = 0
    y = x + 100
    return y


@cython.with_gil
@cython.cfunc
def f_with_gil(x: cython.int) -> cython.int:
    return x + len([1, 2] * x)


def test_with_gil(x: cython.int):
    """
    >>> test_with_gil(3)
    9
    """
    with cython.nogil:
        result = f_with_gil(x)
    return result


@cython.nogil
@cython.exceptval(check=False)
@cython.cfunc
def write_unraisable() -> cython.int:
    with cython.gil:
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
    res: cython.int = 0

    with cython.nogil(True):
        res = f_nogil(res)
        with cython.gil:
            res = f_gil(res)
            with cython.nogil:
                res = f_nogil(res)

        with cython.gil:
            res = f_gil(res)
            with cython.nogil(True):
                res = f_nogil(res)
            with cython.nogil:
                res = f_nogil(res)

    return res


def test_try_finally():
    """
    >>> test_try_finally()
    113
    """
    res: cython.int = 0

    try:
        with cython.nogil(True):
            try:
                res = f_nogil(res)
                with cython.gil:
                    try:
                        res = f_gil(res)
                    finally:
                        res += 1
            finally:
                res = res + 1
    finally:
        res += 1

    return res


number_or_object = cython.fused_type(cython.int, cython.float, object)


def test_fused(x: number_or_object) -> number_or_object:
    """
    >>> test_fused["int"](1)
    2
    >>> test_fused["float"](1.0)
    2.0
    >>> test_fused[object](1)
    2
    >>> test_fused[object](1.0)
    2.0
    """
    res: number_or_object = x

    with cython.nogil(number_or_object is not object):
        res = res + 1

    return res


int_or_object = cython.fused_type(cython.int, object)


def test_fused_object(x: int_or_object):
    """
    >>> import cython
    >>> test_fused_object[object]("spam")
    456
    >>> test_fused_object["int"](1000)
    1000
    """
    res: cython.int = 0

    if int_or_object is object:
        with cython.nogil(False):
            res += len(x)

        try:
            with cython.nogil(int_or_object is object):
                try:
                    with cython.gil(int_or_object is object):
                        res = f_gil(res)
                    with cython.gil:
                        res = f_gil(res)
                    with cython.gil(False):
                        res = f_nogil(res)

                    with cython.gil(int_or_object is not object):
                        res = f_nogil(res)
                    with cython.nogil(False):
                        res = f_nogil(res)

                    res = f_nogil(res)
                finally:
                    res = res + 1

            with cython.nogil(int_or_object is not object):
                res = f_gil(res)

            with cython.gil(int_or_object is not object):
                res = f_gil(res)

                with cython.nogil(int_or_object is object):
                    res = f_nogil(res)

        finally:
            res += 1
    else:
        res = x

    return res


def test_fused_int(x: int_or_object):
    """
    >>> import cython
    >>> test_fused_int[object]("spam")
    4
    >>> test_fused_int["int"](1000)
    1452
    """
    res: cython.int = 0

    if int_or_object is cython.int:
        res += x

        try:
            with cython.nogil(int_or_object is cython.int):
                try:
                    with cython.gil(int_or_object is int):
                        res = f_gil(res)
                    with cython.gil:
                        res = f_gil(res)
                    with cython.gil(False):
                        res = f_nogil(res)

                    with cython.gil(int_or_object is not int):
                        res = f_nogil(res)
                    with cython.nogil(False):
                        res = f_nogil(res)

                    res = f_nogil(res)
                finally:
                    res = res + 1

            with cython.nogil(int_or_object is not cython.int):
                res = f_gil(res)

            with cython.gil(int_or_object is not int):
                res = f_gil(res)

                with cython.nogil(int_or_object is int):
                    res = f_nogil(res)

        finally:
            res += 1
    else:
        with cython.nogil(False):
            res = len(x)

    return res
