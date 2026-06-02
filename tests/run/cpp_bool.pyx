# mode: run
# tag: cpp, werror, no-cpp-locals

from libcpp cimport bool

from typing import Optional

def test_bool(bool a):
    """
    >>> test_bool(True)
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


cdef bool may_raise_exception(bool value, exception) except *:
    if exception:
        raise exception
    else:
        return value

def test_may_raise_exception(bool value, exception=None):
    """
    >>> test_may_raise_exception(False)
    False
    >>> test_may_raise_exception(True)
    True
    >>> test_may_raise_exception(True, RuntimeError)
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    return may_raise_exception(value, exception)

def test_as_annotation(value: Optional[bool]):
    """
    >>> test_as_annotation(True)
    True
    >>> test_as_annotation(None)
    """
    return value
