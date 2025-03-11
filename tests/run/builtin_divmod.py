# mode: run

import cython

def divmod_regular(a, b):
    """
    >>> divmod_regular(10, 5)
    (2, 0)
    >>> divmod_regular(9191, 4096)
    (2, 999)
    >>> divmod_regular(10000, 10010)
    (0, 10000)
    >>> divmod_regular(-999999, -111111)
    (9, 0)
    >>> divmod_regular(-888888, -11111)
    (80, -8)
    >>> divmod_regular(-10000, -10086)
    (0, -10000)
    >>> divmod_regular(5, -1)
    (-5, 0)
    >>> divmod_regular(-40, 3)
    (-14, 2)
    >>> divmod_regular(11, -3)
    (-4, -1)
    >>> divmod_regular(0, 9)
    (0, 0)
    >>> divmod_regular(0, -987654321)
    (0, 0)

    >>> divmod_regular(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    result = divmod(a, b)
    return result


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_int']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_cint(a: cython.int, b: cython.int):
    """
    >>> divmod_cint(10, 5)
    (2, 0)
    >>> divmod_cint(9191, 4096)
    (2, 999)
    >>> divmod_cint(10000, 10010)
    (0, 10000)
    >>> divmod_cint(-999999, -111111)
    (9, 0)
    >>> divmod_cint(-888888, -11111)
    (80, -8)
    >>> divmod_cint(-10000, -10086)
    (0, -10000)
    >>> divmod_cint(-50, 1)
    (-50, 0)
    >>> divmod_cint(-40, 3)
    (-14, 2)
    >>> divmod_cint(11, -3)
    (-4, -1)
    >>> divmod_cint(0, 9)
    (0, 0)
    >>> divmod_cint(0, -987654321)
    (0, 0)

    >>> divmod_cint(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    result = divmod(a, b)
    return result


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_long']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_clong(a: cython.long, b: cython.long):
    """
    >>> divmod_clong(10, 5)
    (2, 0)
    >>> divmod_clong(9191, 4096)
    (2, 999)
    >>> divmod_clong(10000, 10010)
    (0, 10000)
    >>> divmod_clong(-999999, -111111)
    (9, 0)
    >>> divmod_clong(-888888, -11111)
    (80, -8)
    >>> divmod_clong(-10000, -10086)
    (0, -10000)
    >>> divmod_clong(-50, 1)
    (-50, 0)
    >>> divmod_clong(-40, 3)
    (-14, 2)
    >>> divmod_clong(11, -3)
    (-4, -1)
    >>> divmod_clong(0, 9)
    (0, 0)
    >>> divmod_clong(0, -987654321)
    (0, 0)

    >>> divmod_clong(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    result = divmod(a, b)
    return result


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_longlong']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_clonglong(a: cython.longlong, b: cython.longlong):
    """
    >>> divmod_clonglong(10, 5)
    (2, 0)
    >>> divmod_clonglong(9191, 4096)
    (2, 999)
    >>> divmod_clonglong(10000, 10010)
    (0, 10000)
    >>> divmod_clonglong(-999999, -111111)
    (9, 0)
    >>> divmod_clonglong(-888888, -11111)
    (80, -8)
    >>> divmod_clonglong(-10000, -10086)
    (0, -10000)
    >>> divmod_clonglong(-50, 1)
    (-50, 0)
    >>> divmod_clonglong(-40, 3)
    (-14, 2)
    >>> divmod_clonglong(11, -3)
    (-4, -1)
    >>> divmod_clonglong(0, 9)
    (0, 0)
    >>> divmod_clonglong(0, -987654321)
    (0, 0)

    >>> divmod_clonglong(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    result = divmod(a, b)
    return result


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_longlong']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_mixed_cint_clonglong(a: cython.int, b: cython.longlong):
    """
    >>> divmod_mixed_cint_clonglong(10, 5)
    (2, 0)
    >>> divmod_mixed_cint_clonglong(9191, 4096)
    (2, 999)
    >>> divmod_mixed_cint_clonglong(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    result = divmod(a, b)
    return result


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_longlong']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_mixed_clonglong_cint(a: cython.longlong, b: cython.int):
    """
    >>> divmod_mixed_clonglong_cint(10, 5)
    (2, 0)
    >>> divmod_mixed_clonglong_cint(9191, 4096)
    (2, 999)
    >>> divmod_mixed_clonglong_cint(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    result = divmod(a, b)
    return result


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_longlong']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_mixed_unpack(a: cython.longlong, b: cython.int):
    """
    >>> divmod_mixed_unpack(10, 5)
    (2, 0)
    >>> divmod_mixed_unpack(9191, 4096)
    (2, 999)
    >>> divmod_mixed_unpack(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    q, r = divmod(a, b)
    if cython.compiled:
        assert cython.typeof(q) == 'long long', cython.typeof(q)
        assert cython.typeof(r) == 'long long', cython.typeof(r)
    return q, r
