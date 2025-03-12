# mode: run
# cython:infer_types=True

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
    >>> divmod_regular(-1, 10)
    (-1, 9)
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
def divmod_cshort(a: cython.short, b: cython.short):
    """
    >>> divmod_cshort(10, 5)
    (2, 0)
    >>> divmod_cshort(-10, 5)
    (-2, 0)
    >>> divmod_cshort(10, -5)
    (-2, 0)
    >>> divmod_cshort(-50, 1)
    (-50, 0)
    >>> divmod_cshort(-40, 3)
    (-14, 2)
    >>> divmod_cshort(11, -3)
    (-4, -1)
    >>> divmod_cshort(-1, 10)
    (-1, 9)
    >>> divmod_cshort(0, 9)
    (0, 0)

    >>> divmod_cshort(33, 0)  #doctest: +ELLIPSIS
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
    >>> divmod_cint(-10, 5)
    (-2, 0)
    >>> divmod_cint(10, -5)
    (-2, 0)
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
    >>> divmod_cint(-1, 10)
    (-1, 9)
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
    >>> divmod_clong(-10, 5)
    (-2, 0)
    >>> divmod_clong(10, -5)
    (-2, 0)
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
    >>> divmod_clong(-1, 10)
    (-1, 9)
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
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_PY_LONG_LONG']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_clonglong(a: cython.longlong, b: cython.longlong):
    """
    >>> divmod_clonglong(10, 5)
    (2, 0)
    >>> divmod_clonglong(-10, 5)
    (-2, 0)
    >>> divmod_clonglong(10, -5)
    (-2, 0)
    >>> divmod_clonglong(9191, 4096)
    (2, 999)
    >>> divmod_clonglong(10000, 10010)
    (0, 10000)
    >>> divmod_clonglong(88321773, 98539211)
    (0, 88321773)
    >>> divmod_clonglong(-99999999, -11111111)
    (9, 0)
    >>> divmod_clonglong(-88888888, -1111111)
    (80, -8)
    >>> divmod_clonglong(-88837244, -110119120)
    (0, -88837244)
    >>> divmod_clonglong(-5000000, 1)
    (-5000000, 0)
    >>> divmod_clonglong(-100190, 17)
    (-5894, 8)
    >>> divmod_clonglong(2014014349, -19)
    (-106000756, -15)
    >>> divmod_clonglong(0, 996007985)
    (0, 0)
    >>> divmod_clonglong(-10000, -10086)
    (0, -10000)
    >>> divmod_clonglong(-50, 1)
    (-50, 0)
    >>> divmod_clonglong(-40, 3)
    (-14, 2)
    >>> divmod_clonglong(11, -3)
    (-4, -1)
    >>> divmod_clonglong(-1, 10)
    (-1, 9)
    >>> divmod_clonglong(0, 9)
    (0, 0)
    >>> divmod_clonglong(0, -987654321)
    (0, 0)

    >>> divmod_clonglong(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    >>> divmod_clonglong(0, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    result = divmod(a, b)
    return result


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_PY_LONG_LONG']",
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
    >>> divmod_mixed_cint_clonglong(0, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    result = divmod(a, b)
    return result


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_PY_LONG_LONG']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_mixed_clonglong_cint(a: cython.longlong, b: cython.int):
    """
    >>> divmod_mixed_clonglong_cint(10, 5)
    (2, 0)
    >>> divmod_mixed_clonglong_cint(9191, 4096)
    (2, 999)
    >>> divmod_mixed_clonglong_cint(19283090123, 1230912)
    (15665, 853643)

    >>> divmod_mixed_clonglong_cint(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    >>> divmod_mixed_clonglong_cint(0, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    result = divmod(a, b)
    return result


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_PY_LONG_LONG']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_mixed_unpack(a: cython.longlong, b: cython.int):
    """
    >>> divmod_mixed_unpack(10, 5)
    (2, 0)
    >>> divmod_mixed_unpack(9191, 4096)
    (2, 999)
    >>> divmod_mixed_unpack(19283090123, 1230912)
    (15665, 853643)

    >>> divmod_mixed_unpack(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    >>> divmod_mixed_unpack(0, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    q, r = divmod(a, b)
    if cython.compiled:
        assert cython.typeof(q) == 'long long', cython.typeof(q)
        assert cython.typeof(r) == 'long long', cython.typeof(r)
    return q, r
