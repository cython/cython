# tag: cpp

from libcpp cimport bool

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
