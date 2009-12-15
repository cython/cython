
def test(**kw):
    """
    >>> d = {1 : 2}
    >>> test(**d)
    Traceback (most recent call last):
    TypeError: test() keywords must be strings
    >>> d
    {1: 2}
    >>> d = {}
    >>> test(**d)
    {'arg': 3}
    >>> d
    {}
    >>> d = {'arg' : 2} # this should be u'arg', but Py2 can't handle it...
    >>> test(**d)
    {'arg': 3}
    >>> d
    {'arg': 2}
    """
    kw['arg'] = 3
    return kw
