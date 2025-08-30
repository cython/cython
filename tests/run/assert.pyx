# mode: run

cimport cython

@cython.test_assert_path_exists(
    '//AssertStatNode',
    '//AssertStatNode//RaiseStatNode',
)
def f(a, b, int i):
    """
    >>> f(1, 2, 1)
    >>> f(0, 2, 1)
    Traceback (most recent call last):
    AssertionError
    >>> f(1, -1, 1)
    Traceback (most recent call last):
    AssertionError
    >>> f(1, 2, 0)
    Traceback (most recent call last):
    AssertionError
    """
    assert a
    assert a+b
    assert i


@cython.test_assert_path_exists(
    '//AssertStatNode',
    '//AssertStatNode//RaiseStatNode',
    '//AssertStatNode//RaiseStatNode//TupleNode',
)
def g(a, b):
    """
    >>> g(1, "works")
    >>> g(0, "fails")
    Traceback (most recent call last):
    AssertionError: fails
    >>> g(0, (1, 2))
    Traceback (most recent call last):
    AssertionError: (1, 2)
    """
    assert a, b


@cython.test_assert_path_exists(
    '//AssertStatNode',
    '//AssertStatNode//RaiseStatNode',
    '//AssertStatNode//RaiseStatNode//TupleNode',
)
def g(a, b):
    """
    >>> g(1, "works")
    >>> g(0, "fails")
    Traceback (most recent call last):
    AssertionError: fails
    >>> g(0, (1, 2))
    Traceback (most recent call last):
    AssertionError: (1, 2)
    """
    assert a, b


@cython.test_assert_path_exists(
    '//AssertStatNode',
    '//AssertStatNode//RaiseStatNode',
    '//AssertStatNode//RaiseStatNode//TupleNode',
    '//AssertStatNode//RaiseStatNode//TupleNode//TupleNode',)
def assert_with_tuple_arg(a):
    """
    >>> assert_with_tuple_arg(True)
    >>> assert_with_tuple_arg(False)
    Traceback (most recent call last):
    AssertionError: (1, 2)
    """
    assert a, (1, 2)


@cython.test_assert_path_exists(
    '//AssertStatNode',
    '//AssertStatNode//RaiseStatNode',
)
@cython.test_fail_if_path_exists(
    '//AssertStatNode//TupleNode',
)
def assert_with_str_arg(a):
    """
    >>> assert_with_str_arg(True)
    >>> assert_with_str_arg(False)
    Traceback (most recent call last):
    AssertionError: abc
    """
    assert a, 'abc'
