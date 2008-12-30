__doc__ = u"""
    >>> f(0,0)
    0
    >>> f(1,2)
    2
    >>> f(1,-1)
    1

    >>> g(1,2)
    1
    >>> g(0,2)
    2
    >>> g(0,0)
    0

    >>> h(1,2)
    1
    >>> h(0,2)
    2
    >>> h(0,0)
    3

    >>> i(1,2)
    1
    >>> i(2,2)
    2
    >>> i(2,1)
    0
"""

def f(a, b):
    x = 0
    if a:
        x = 1
    if a+b:
        x = 2
    return x

def g(a, b):
    x = 0
    if a:
        x = 1
    elif b:
        x = 2
    return x
    
def h(a, b):
    x = 0
    if a:
        x = 1
    elif b:
        x = 2
    else:
        x = 3
    return x

try:
    import __builtin__  as builtins
except ImportError:
    import builtins

def i(a, b):
    x = 0
    if builtins.str(a).upper() == u"1":
        x = 1
    if builtins.str(a+b).lower() not in (u"1", u"3"):
        x = 2
    return x
