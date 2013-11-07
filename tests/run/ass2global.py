__doc__ = u"""
    >>> getg()
    5
    >>> f(42)
    >>> getg()
    42
    >>> global_in_class
    9
"""

g = 5


def f(a):
    global g
    g = a


def getg():
    return g


class Test(object):
    global global_in_class
    global_in_class = 9
