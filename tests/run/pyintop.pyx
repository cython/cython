def f(obj1, obj2, obj3):
    """
    >>> f(1,2,3)
    3
    """
    obj1 = obj2 | obj3
    return obj1

def g(obj1, obj2, obj3):
    """
    >>> g(1,2,3)
    1
    """
    obj1 = obj2 ^ obj3
    return obj1

def h(obj1, obj2, obj3):
    """
    >>> h(1,2,3)
    2
    """
    obj1 = obj2 & obj3
    return obj1

def j(obj1, obj2, obj3):
    """
    >>> j(1,2,3)
    16
    """
    obj1 = obj2 << obj3
    return obj1

def k(obj1, obj2, obj3):
    """
    >>> k(1,2,3)
    0
    """
    obj1 = obj2 >> obj3
    return obj1

def l(obj1, obj2, obj3):
    """
    >>> l(1,2,3)
    16
    """
    obj1 = obj2 << obj3 | obj2 >> obj3
    return obj1
