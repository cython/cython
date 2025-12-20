
__doc__ = """
>>> it = iter([1,2,3])
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

>>> next(it, 123)
123

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
    >>> test_single_next(it)  # 1
    1
    >>> test_single_next(it)  # 2
    2
    >>> test_single_next(it)  # 3
    3
    >>> test_single_next(it)  # 4
    Traceback (most recent call last):
    StopIteration
    >>> test_single_next(it)
    Traceback (most recent call last):
    StopIteration

    >>> class It:
    ...     def __init__(self, value):
    ...         self.value = value
    ...     def __next__(self):
    ...         raise StopIteration(self.value)

    # Assert that the StopIteration value doesn't get lost.
    >>> test_single_next(It(42))
    Traceback (most recent call last):
    StopIteration: 42
    """
    return next(it)

def test_default_next(it, default):
    """
    >>> it = iter([1,2,3])
    >>> test_default_next(it, 99)  # 1
    1
    >>> test_default_next(it, 99)  # 2
    2
    >>> test_default_next(it, 99)  # 3
    3
    >>> test_default_next(it, 99)  # 4
    99
    >>> test_default_next(it, 99)  # 5
    99
    """
    return next(it, default)

def test_next_override(it):
    """
    >>> it = iter([1,2,3])
    >>> test_next_override(it)  # 1
    1
    >>> test_next_override(it)  # 2
    1
    >>> test_next_override(it)  # 3
    1
    >>> test_next_override(it)  # 4
    1
    """
    def next(it):
        return 1
    return next(it)
