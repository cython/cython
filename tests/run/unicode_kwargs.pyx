# -*- coding: utf8 -*-

try:
    import platform
    IS_PYPY = platform.python_implementation() == 'PyPy'
except (ImportError, AttributeError):
    IS_PYPY = False

ustring_a = u'a'
ustring_ascii = u'abc'
ustring_nonascii = u'àöé\u0888'


def accept_kwargs(a, b, c=1, **kwargs):
    """
    >>> accept_kwargs(1, 2, 3)
    (1, 2, 3, {})
    >>> accept_kwargs(1, 2, 3, d=5)
    (1, 2, 3, {'d': 5})

    >>> accept_kwargs(1, 2, 3, **{ustring_a: 5})
    Traceback (most recent call last):
    TypeError: accept_kwargs() got multiple values for keyword argument 'a'

    >>> if not IS_PYPY: a, b, c, kwargs = accept_kwargs(1, 2, 3, **{ustring_ascii: 5})
    >>> IS_PYPY and (1,2,3,1) or (a,b,c,len(kwargs))
    (1, 2, 3, 1)
    >>> IS_PYPY and 5 or kwargs[ustring_ascii]
    5

    >>> if not IS_PYPY: a, b, c, kwargs = accept_kwargs(1, 2, 3, **{ustring_nonascii: 5})
    >>> IS_PYPY and (1,2,3,1) or (a,b,c,len(kwargs))
    (1, 2, 3, 1)
    >>> IS_PYPY and 5 or kwargs[ustring_nonascii]
    5

    >>> if not IS_PYPY: a, b, c, kwargs = accept_kwargs(1, 2, 3, **{ustring_nonascii: 5, ustring_ascii: 6})
    >>> IS_PYPY and (1,2,3,2) or (a,b,c,len(kwargs))
    (1, 2, 3, 2)
    >>> IS_PYPY and 5 or kwargs[ustring_nonascii]
    5
    >>> IS_PYPY and 6 or kwargs[ustring_ascii]
    6
    """
    return a, b, c, kwargs

def unexpected_kwarg(a, b, c=1):
    """
    >>> unexpected_kwarg(1, b=2)
    (1, 2, 1)
    >>> unexpected_kwarg(1, 2, **{ustring_ascii: 5})
    Traceback (most recent call last):
    TypeError: unexpected_kwarg() got an unexpected keyword argument 'abc'
    >>> unexpected_kwarg(1, 2, 3, d=5)
    Traceback (most recent call last):
    TypeError: unexpected_kwarg() got an unexpected keyword argument 'd'
    """
    return a, b, c
