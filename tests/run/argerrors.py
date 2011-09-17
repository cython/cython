# mode: run

def test_single_arg(a):
    """
    >>> test_single_arg(1)
    1
    >>> test_single_arg()                # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> test_single_arg(1,2)             # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> test_single_arg(**{})            # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> test_single_arg(*(), **{})       # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    return a

def test_two_args(a,b):
    """
    >>> test_two_args(1,2)
    (1, 2)
    >>> test_two_args()              # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> test_two_args(1)             # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> test_two_args(1,2,3)         # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> test_two_args(**{})          # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> test_two_args(1, **{})       # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> test_two_args(*(), **{})     # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    return a,b
