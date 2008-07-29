__doc__ = u"""
    >>> f(1, 2, 3, 4, 5)
    []
    >>> g(1, 2, 3, 4, 5)
    [2]
    >>> h(1, 2, 3, 4, 5)
    [2, 3]
    >>> j(1, 2, 3, 4, 5)
    [2, 3, 4]
    >>> k(1, 2, 3, 4, 5)
    [17, 42, 88]
"""

def f(obj1, obj2, obj3, obj4, obj5):
    obj1 = []
    return obj1

def g(obj1, obj2, obj3, obj4, obj5):
    obj1 = [obj2]
    return obj1

def h(obj1, obj2, obj3, obj4, obj5):
    obj1 = [obj2, obj3]
    return obj1

def j(obj1, obj2, obj3, obj4, obj5):
    obj1 = [obj2, obj3, obj4]
    return obj1

def k(obj1, obj2, obj3, obj4, obj5):
    obj1 = [17, 42, 88]
    return obj1
