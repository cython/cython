def f():
    """
    >>> f()
    6
    """
    obj1 = 1
    obj2 = 2
    obj3 = 3
    obj1 = obj2 * obj3
    return obj1

def g():
    """
    >>> g()
    2
    """
    obj1 = 12
    obj2 = 6
    obj3 = 3
    obj1 = obj2 / obj3
    return int(obj1)
