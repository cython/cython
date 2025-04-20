# mode: run
# cython:infer_types=True

cimport cython

from libc.stdint cimport int64_t


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_int64_t']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_typedef(a: int64_t, b: cython.int):
    """
    >>> divmod_typedef(10, 5)
    (2, 0)
    >>> divmod_typedef(9191, 4096)
    (2, 999)
    >>> divmod_typedef(-420000000000, 1000)
    (-420000000, 0)

    >>> divmod_typedef(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    >>> divmod_typedef(0, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    result = divmod(a, b)
    return result


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_int64_t']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_typedef_const(a: int64_t):
    """
    >>> divmod_typedef_const(10)
    (0, 10)
    >>> divmod_typedef_const(9191)
    (9, 191)
    >>> divmod_typedef_const(-420000000000)
    (-420000000, 0)
    """
    result = divmod(a, 1000)
    return result
