__doc__ = """
    >>> l = [1,2,3,4]

    >>> f(1, l, 2, 3)
    [1, 2, 3, 4]
    >>> l == f(1, l, 2, 3)
    True
    >>> l is f(1, l, 2, 3)
    False

    >>> g(1, [1,2,3,4], 2, 3)
    [3, 4]

    >>> h(1, [1,2,3,4], 2, 3)
    [1, 2, 3]

    >>> j(1, [1,2,3,4], 2, 3)
    [3]
"""

def f(obj1, obj2, obj3, obj4):
    obj1 = obj2[:]
    return obj1

def g(obj1, obj2, obj3, obj4):
    obj1 = obj2[obj3:]
    return obj1

def h(obj1, obj2, obj3, obj4):
    obj1 = obj2[:obj4]
    return obj1

def j(obj1, obj2, obj3, obj4):
    obj1 = obj2[obj3:obj4]
    return obj1
