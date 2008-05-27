__doc__ = u"""
    >>> f()
    6
    >>> g()
    2
"""

def f():
    obj1 = 1
    obj2 = 2
    obj3 = 3
    obj1 = obj2 * obj3
    return obj1

def g():
    obj1 = 12
    obj2 = 6
    obj3 = 3
    obj1 = obj2 / obj3
    return int(obj1)
