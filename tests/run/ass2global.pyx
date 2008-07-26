__doc__ = u"""
    >>> getg()
    5
    >>> f(42)
    >>> getg()
    42
"""

g = 5

def f(a):
    global g
    g = a

def getg():
    return g
