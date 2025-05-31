# mode: run

"""
Tests for assorted builtin functions that do not merit their own test file.
"""

import cython
from cython import typeof


def test_format():
    """
    >>> test_format()
    ('123', '7b')
    """
    s1 = format(123)
    assert typeof(s1) == 'str object', typeof(s1)
    s2 = format(123, 'x')
    assert typeof(s2) == 'str object', typeof(s2)
    return s1, s2


def test_hex(n):
    """
    >>> test_hex(5)
    '0x5'
    >>> test_hex(55)
    '0x37'
    >>> test_hex('abc')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    s = hex(n)
    assert typeof(s) == 'str object', typeof(s)
    return s


def test_oct(n):
    """
    >>> test_oct(5)
    '0o5'
    >>> test_oct(55)
    '0o67'
    >>> test_oct('abc')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    s = oct(n)
    assert typeof(s) == 'str object', typeof(s)
    return s
