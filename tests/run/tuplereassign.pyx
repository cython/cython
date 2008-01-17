__doc__ = """
    >>> test1( (1,2,3) )
    1
    >>> test3( (1,2,3) )
    3
    >>> test( (1,2,3) )
    3
"""

def test1(t):
    t,a,b = t
    return t

def test3(t):
    a,b,t = t
    return t

def test(t):
    t,t,t = t
    return t
