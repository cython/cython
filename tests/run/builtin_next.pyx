
import sys
IS_PY3 = sys.version_info[0] >= 3

__doc__ = """
>>> it = iter([1,2,3])
>>> if not IS_PY3:
...     next = type(it).next
>>> next(it)
1
>>> next(it)
2
>>> next(it)
3

>>> next(it)
Traceback (most recent call last):
StopIteration

>>> next(it)
Traceback (most recent call last):
StopIteration

>>> if IS_PY3: next(it, 123)
... else: print(123)
123
"""

if IS_PY3:
    __doc__ += """
>>> next(123)      # doctest: +ELLIPSIS
Traceback (most recent call last):
TypeError: ...int... object is not an iterator
"""

def test_next_not_iterable(it):
    """
    >>> test_next_not_iterable(123)
    Traceback (most recent call last):
    TypeError: int object is not an iterator
    """
    return next(it)

def test_single_next(it):
    """
    >>> it = iter([1,2,3])
    >>> test_single_next(it)
    1
    >>> test_single_next(it)
    2
    >>> test_single_next(it)
    3
    >>> test_single_next(it)
    Traceback (most recent call last):
    StopIteration
    >>> test_single_next(it)
    Traceback (most recent call last):
    StopIteration
    """
    return next(it)

def test_default_next(it, default):
    """
    >>> it = iter([1,2,3])
    >>> test_default_next(it, 99)
    1
    >>> test_default_next(it, 99)
    2
    >>> test_default_next(it, 99)
    3
    >>> test_default_next(it, 99)
    99
    >>> test_default_next(it, 99)
    99
    """
    return next(it, default)

def test_next_override(it):
    """
    >>> it = iter([1,2,3])
    >>> test_next_override(it)
    1
    >>> test_next_override(it)
    1
    >>> test_next_override(it)
    1
    >>> test_next_override(it)
    1
    """
    def next(it):
        return 1
    return next(it)
