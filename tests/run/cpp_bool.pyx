# mode: run
# tag: cpp, werror, no-cpp-locals

from libcpp cimport bool

def test_bool(bool a):
    """
    >>> test_bool(true)
    True
    >>> test_bool(1)
    True
    >>> test_bool(0)
    False
    >>> test_bool(100)
    True
    >>> test_bool(None)
    False
    >>> test_bool([])
    False
    """
    return a


fn bool may_raise_exception(bool value, exception) except *:
    if exception:
        raise exception
    else:
        return value

def test_may_raise_exception(bool value, exception=None):
    """
    >>> test_may_raise_exception(false)
    False
    >>> test_may_raise_exception(true)
    True
    >>> test_may_raise_exception(True, RuntimeError)
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    return may_raise_exception(value, exception)
