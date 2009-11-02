import sys

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
    if sys.version_info[0] >= 3:
        kw[u'arg'] = 3
    else:
        kw['arg'] = 3
    return kw
