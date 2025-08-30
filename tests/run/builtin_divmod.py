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

    >>> divmod_regular(10.0, 5)
    (2.0, 0.0)
    >>> divmod_regular(10, 5.0)
    (2.0, 0.0)
    >>> divmod_regular(10.0, 5.0)
    (2.0, 0.0)
    >>> divmod_regular(9191.0, 4096)
    (2.0, 999.0)
    >>> divmod_regular(9191, 4096.0)
    (2.0, 999.0)
    >>> divmod_regular(9191.0, 4096.0)
    (2.0, 999.0)

    >>> divmod_regular(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    >>> divmod_regular(33.0, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    result = divmod(a, b)
    return result


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_int_short']",
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
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_int_int']",
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
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_int_long']",
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
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_int_PY_LONG_LONG']",
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
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_int_PY_LONG_LONG']",
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
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_int_PY_LONG_LONG']",
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
    >>> divmod_mixed_clonglong_cint(-420000000000, 1000)
    (-420000000, 0)

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
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_int_PY_LONG_LONG']",
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


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_int_PY_LONG_LONG']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_mixed_const(a: cython.longlong):
    """
    >>> divmod_mixed_const(-420000000000)
    (-420000000, 0)
    >>> divmod_mixed_const(9191)
    (9, 191)
    >>> divmod_mixed_const(19283090123)
    (19283090, 123)
    """
    q, r = divmod(a, 1000)
    if cython.compiled:
        assert cython.typeof(q) == 'long long', cython.typeof(q)
        assert cython.typeof(r) == 'long long', cython.typeof(r)
    return q, r


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_float_double']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_cfloat(a: cython.float, b: cython.float):
    """
    >>> divmod_cfloat(10.0, 5.0)
    (2.0, 0.0)
    >>> divmod_cfloat(-10.0, 5.0)
    (-2.0, 0.0)
    >>> divmod_cfloat(10.0, -5.0)
    (-2.0, -0.0)
    >>> divmod_cfloat(9191.0, 4096.0)
    (2.0, 999.0)
    >>> divmod_cfloat(10000.0, 10010.0)
    (0.0, 10000.0)
    >>> divmod_cfloat(-999999.0, -111111.0)
    (9.0, -0.0)
    >>> divmod_cfloat(-888888.0, -11111.0)
    (80.0, -8.0)
    >>> divmod_cfloat(-10000.0, -10086.0)
    (0.0, -10000.0)
    >>> divmod_cfloat(-50.0, 1.0)
    (-50.0, 0.0)
    >>> divmod_cfloat(-40.0, 3.0)
    (-14.0, 2.0)
    >>> divmod_cfloat(11.0, -3.0)
    (-4.0, -1.0)
    >>> divmod_cfloat(-1.0, 10.0)
    (-1.0, 9.0)
    >>> divmod_cfloat(0.0, 9.0)
    (0.0, 0.0)
    >>> divmod_cfloat(0.0, -987654321.0)
    (-0.0, -0.0)

    >>> divmod_cfloat(33.0, 0.0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    result = divmod(a, b)
    return result


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_float_double']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_cdouble(a: cython.double, b: cython.double):
    """
    >>> divmod_cdouble(10.0, 5.0)
    (2.0, 0.0)
    >>> divmod_cdouble(-10.0, 5.0)
    (-2.0, 0.0)
    >>> divmod_cdouble(10.0, -5.0)
    (-2.0, -0.0)
    >>> divmod_cdouble(9191.0, 4096.0)
    (2.0, 999.0)
    >>> divmod_cdouble(10000.0, 10010.0)
    (0.0, 10000.0)
    >>> divmod_cdouble(-999999.0, -111111.0)
    (9.0, -0.0)
    >>> divmod_cdouble(-888888.0, -11111.0)
    (80.0, -8.0)
    >>> divmod_cdouble(-10000.0, -10086.0)
    (0.0, -10000.0)
    >>> divmod_cdouble(-50.0, 1.0)
    (-50.0, 0.0)
    >>> divmod_cdouble(-40.0, 3.0)
    (-14.0, 2.0)
    >>> divmod_cdouble(11.0, -3.0)
    (-4.0, -1.0)
    >>> divmod_cdouble(-1.0, 10.0)
    (-1.0, 9.0)
    >>> divmod_cdouble(0.0, 9.0)
    (0.0, 0.0)
    >>> divmod_cdouble(0.0, -987654321.0)
    (-0.0, -0.0)

    >>> divmod_cdouble(33.0, 0.0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    result = divmod(a, b)
    return result


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_float_double']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_clongdouble(a: cython.longdouble, b: cython.double):
    """
    >>> divmod_clongdouble(10.0, 5.0)
    (2.0, 0.0)
    >>> divmod_clongdouble(-10.0, 5.0)
    (-2.0, 0.0)
    >>> divmod_clongdouble(10.0, -5.0)
    (-2.0, -0.0)
    >>> divmod_clongdouble(9191.0, 4096.0)
    (2.0, 999.0)
    >>> divmod_clongdouble(10000.0, 10010.0)
    (0.0, 10000.0)
    >>> divmod_clongdouble(-999999.0, -111111.0)
    (9.0, -0.0)
    >>> divmod_clongdouble(-888888.0, -11111.0)
    (80.0, -8.0)
    >>> divmod_clongdouble(-10000.0, -10086.0)
    (0.0, -10000.0)
    >>> divmod_clongdouble(-50.0, 1.0)
    (-50.0, 0.0)
    >>> divmod_clongdouble(-40.0, 3.0)
    (-14.0, 2.0)
    >>> divmod_clongdouble(11.0, -3.0)
    (-4.0, -1.0)
    >>> divmod_clongdouble(-1.0, 10.0)
    (-1.0, 9.0)
    >>> divmod_clongdouble(0.0, 9.0)
    (0.0, 0.0)
    >>> divmod_clongdouble(0.0, -987654321.0)
    (-0.0, -0.0)

    >>> divmod_clongdouble(33.0, 0.0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    result = divmod(a, b)
    return result


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_float_double']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_mixed_cdouble(a: cython.double, b: cython.float):
    """
    >>> divmod_mixed_cdouble(10.0, 5.0)
    (2.0, 0.0)
    >>> divmod_mixed_cdouble(-10.0, 5.0)
    (-2.0, 0.0)
    >>> divmod_mixed_cdouble(10.0, -5.0)
    (-2.0, -0.0)
    >>> divmod_mixed_cdouble(9191.0, 4096.0)
    (2.0, 999.0)
    >>> divmod_mixed_cdouble(10000.0, 10010.0)
    (0.0, 10000.0)
    >>> divmod_mixed_cdouble(-999999.0, -111111.0)
    (9.0, -0.0)
    >>> divmod_mixed_cdouble(-888888.0, -11111.0)
    (80.0, -8.0)
    >>> divmod_mixed_cdouble(-10000.0, -10086.0)
    (0.0, -10000.0)
    >>> divmod_mixed_cdouble(-50.0, 1.0)
    (-50.0, 0.0)
    >>> divmod_mixed_cdouble(-40.0, 3.0)
    (-14.0, 2.0)
    >>> divmod_mixed_cdouble(11.0, -3.0)
    (-4.0, -1.0)
    >>> divmod_mixed_cdouble(-1.0, 10.0)
    (-1.0, 9.0)
    >>> divmod_mixed_cdouble(0.0, 9.0)
    (0.0, 0.0)
    >>> divmod_mixed_cdouble(0.0, -987654321.0)
    (-0.0, -0.0)

    >>> divmod_mixed_cdouble(33.0, 0.0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    result = divmod(a, b)
    return result


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_nogil_int_long']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_int_nogil(a: cython.long, b: cython.int):
    """
    >>> divmod_int_nogil(10, 5)
    (2, 0)
    >>> divmod_int_nogil(-10, 5)
    (-2, 0)
    >>> divmod_int_nogil(9191, 4096)
    (2, 999)

    >>> divmod_int_nogil(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    >>> divmod_int_nogil(0, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    with cython.nogil:
        q, r = divmod(a, b)
    return q, r


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_nogil_float_double']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_float_nogil(a: cython.float, b: cython.double):
    """
    >>> divmod_float_nogil(10.0, 5.0)
    (2.0, 0.0)
    >>> divmod_float_nogil(-10.0, 5.0)
    (-2.0, 0.0)
    >>> divmod_float_nogil(9191.0, 4096.0)
    (2.0, 999.0)

    >>> divmod_float_nogil(33.0, 0.0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    >>> divmod_float_nogil(0.0, 0.0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    with cython.nogil:
        q, r = divmod(a, b)
    return q, r
