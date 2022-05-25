cimport cython


def generator():
    yield 2
    yield 1
    yield 3


def returns_set():
    return {"foo", "bar", "baz"}


def returns_tuple():
    return (1, 2, 3, 0)


@cython.test_fail_if_path_exists("//SimpleCallNode")
def sorted_arg(x):
    """
    >>> a = [3, 2, 1]
    >>> sorted_arg(a)
    [1, 2, 3]
    >>> a
    [3, 2, 1]
    >>> sorted(generator())
    [1, 2, 3]
    >>> sorted(returns_set())
    ['bar', 'baz', 'foo']
    >>> sorted(returns_tuple())
    [0, 1, 2, 3]
    >>> sorted(object())
    Traceback (most recent call last):
    TypeError: 'object' object is not iterable
    """
    return sorted(x)


@cython.test_assert_path_exists("//GeneralCallNode")
def sorted_arg_with_key(x):
    """
    >>> a = [3, 2, 1]
    >>> sorted_arg_with_key(a)
    [3, 2, 1]
    >>> a
    [3, 2, 1]
    >>> sorted_arg_with_key(generator())
    [3, 2, 1]
    >>> sorted_arg_with_key(returns_tuple())
    [3, 2, 1, 0]
    >>> sorted_arg_with_key(object())
    Traceback (most recent call last):
    TypeError: 'object' object is not iterable
    """
    return sorted(x, key=lambda x: -x)


@cython.test_fail_if_path_exists("//YieldExprNode",
                                 "//NoneCheckNode")
@cython.test_assert_path_exists("//InlinedGeneratorExpressionNode")
def sorted_genexp():
    """
    >>> sorted_genexp()
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    """
    return sorted(i*i for i in range(10,0,-1))


@cython.test_fail_if_path_exists("//SimpleCallNode//SimpleCallNode")
@cython.test_assert_path_exists("//SimpleCallNode/NameNode[@name = 'range']")
def sorted_list_of_range():
    """
    >>> sorted_list_of_range()
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    return sorted(list(range(10,0,-1)))


@cython.test_fail_if_path_exists("//SimpleCallNode")
def sorted_list_literal():
    """
    >>> sorted_list_literal()
    [1, 1, 2, 2, 3, 3]
    """
    return sorted([3, 1, 2] * 2)


@cython.test_fail_if_path_exists("//SimpleCallNode")
def sorted_tuple_literal():
    """
    >>> sorted_tuple_literal()
    [1, 1, 2, 2, 3, 3]
    """
    return sorted((1, 3, 2) * 2)
