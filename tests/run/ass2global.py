"""
    >>> getg()
    5
    >>> setg(42)
    >>> getg()
    42
"""

g = 5


def setg(a):
    global g
    g = a


def getg():
    return g


class Test(object):
    """
    >>> global_in_class
    9
    >>> Test.global_in_class
    Traceback (most recent call last):
    AttributeError: type object 'Test' has no attribute 'global_in_class'
    >>> Test().global_in_class
    Traceback (most recent call last):
    AttributeError: 'Test' object has no attribute 'global_in_class'
    """
    global global_in_class
    global_in_class = 9
