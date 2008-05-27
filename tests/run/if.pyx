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
