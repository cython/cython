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


def test_ascii(n):
    """
    >>> ascii(5)
    '5'
    >>> test_ascii(5)
    '5'

    >>> ascii('\\N{SNOWMAN}')
    "'\\\\u2603'"
    >>> test_ascii('\\N{SNOWMAN}')
    "'\\\\u2603'"
    """
    s = ascii(n)
    assert typeof(s) == 'str object', typeof(s)
    return s


def test_bin(n):
    """
    >>> bin(5)
    '0b101'
    >>> test_bin(5)
    '0b101'

    >>> bin(55)
    '0b110111'
    >>> test_bin(55)
    '0b110111'

    >>> bin('abc')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> test_bin('abc')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    s = bin(n)
    assert typeof(s) == 'str object', typeof(s)
    return s


def test_hex(n):
    """
    >>> hex(5)
    '0x5'
    >>> test_hex(5)
    '0x5'

    >>> hex(55)
    '0x37'
    >>> test_hex(55)
    '0x37'

    >>> hex('abc')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> test_hex('abc')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    s = hex(n)
    assert typeof(s) == 'str object', typeof(s)
    return s


def test_oct(n):
    """
    >>> oct(5)
    '0o5'
    >>> test_oct(5)
    '0o5'

    >>> test_oct(55)
    '0o67'
    >>> oct(55)
    '0o67'

    >>> oct('abc')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> test_oct('abc')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    s = oct(n)
    assert typeof(s) == 'str object', typeof(s)
    return s
