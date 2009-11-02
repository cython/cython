def test1(t):
    """
    >>> test1( (1,2,3) )
    1
    """
    t,a,b = t
    return t

def test3(t):
    """
    >>> test3( (1,2,3) )
    3
    """
    a,b,t = t
    return t

def test(t):
    """
    >>> test( (1,2,3) )
    3
    """
    t,t,t = t
    return t

def testnonsense():
    """
    >>> testnonsense()     # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    t,t,t = 1*2
    return t
