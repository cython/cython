__doc__ = """
    >>> f()
    6
    >>> g()
    0
"""

def f():
    obj1 = 1
    obj2 = 2
    obj3 = 3
    obj1 = obj2 * obj3
    return obj1

def g():
    obj1 = 1
    obj2 = 2
    obj3 = 3
    obj1 = obj2 / obj3
    return obj1
