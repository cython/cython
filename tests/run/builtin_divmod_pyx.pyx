# mode: run
# cython:infer_types=True

cimport cython

from libc.stdint cimport int64_t


### Tests for external typedefs.

@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_int_td_int64_t']",
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
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_int_td_int64_t']",
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


### Tests for internal and mixed typedefs.

ctypedef long my_long_type
ctypedef int64_t my_int64_type


@cython.test_assert_path_exists(
    "//SimpleCallNode//NameNode[@entry.name = 'divmod']",
    "//SimpleCallNode//NameNode[@entry.cname = '__Pyx_divmod_int_td_int64_t']",
    "//ReturnStatNode//CoerceToPyTypeNode",
)
def divmod_typedef_mixed(a: my_int64_type, b: cython.int):
    """
    >>> divmod_typedef_mixed(10, 5)
    (2, 0)
    >>> divmod_typedef_mixed(9191, 4096)
    (2, 999)
    >>> divmod_typedef_mixed(-420000000000, 1000)
    (-420000000, 0)

    >>> divmod_typedef_mixed(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    >>> divmod_typedef_mixed(0, 0)  #doctest: +ELLIPSIS
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
def divmod_typedef_internal(a: my_long_type, b: cython.int):
    """
    >>> divmod_typedef_internal(10, 5)
    (2, 0)
    >>> divmod_typedef_internal(9191, 4096)
    (2, 999)

    >>> divmod_typedef_internal(33, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    >>> divmod_typedef_internal(0, 0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    """
    result = divmod(a, b)
    return result
