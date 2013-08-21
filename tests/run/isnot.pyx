# mode: run
# tag: is_not

cimport cython

@cython.test_fail_if_path_exists('//NotNode')
def is_not(a, b):
    """
    >>> is_not(1, 2)
    True
    >>> x = 1
    >>> is_not(x, x)
    False
    """
    return a is not b


@cython.test_fail_if_path_exists('//NotNode')
def not_is_not(a, b):
    """
    >>> not_is_not(1, 2)
    False
    >>> x = 1
    >>> not_is_not(x, x)
    True
    """
    return not a is not b


@cython.test_fail_if_path_exists('//NotNode')
def not_is(a, b):
    """
    >>> not_is(1, 2)
    True
    >>> x = 1
    >>> not_is(x, x)
    False
    """
    return not a is b


@cython.test_fail_if_path_exists('//NotNode')
def is_not_None(a):
    """
    >>> is_not_None(1)
    True
    >>> is_not_None(None)
    False
    """
    return a is not None


@cython.test_fail_if_path_exists('//NotNode')
def not_is_not_None(a):
    """
    >>> not_is_not_None(1)
    False
    >>> not_is_not_None(None)
    True
    """
    return not a is not None


@cython.test_fail_if_path_exists('//NotNode')
def not_is_None(a):
    """
    >>> not_is_None(1)
    True
    >>> not_is_None(None)
    False
    """
    return not a is None
