
def test(**kw):
    """
    >>> d = {1 : 2}
    >>> test(**d)       # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...keywords must be strings
    >>> d
    {1: 2}
    >>> d = {}
    >>> test(**d)
    {'arg': 3}
    >>> d
    {}
    >>> d = {'arg' : 2}
    >>> test(**d)
    {'arg': 3}
    >>> d
    {'arg': 2}
    """
    kw['arg'] = 3
    return kw
