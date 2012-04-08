def f(obj1, obj2, obj3, obj4):
    """
    >>> l = [1,2,3,4]
    >>> f(1, l, 2, 3)
    [1, 2, 3, 4]
    >>> l == f(1, l, 2, 3)
    True
    >>> l is f(1, l, 2, 3)
    False
    >>> try: f(1, 42, 2, 3)
    ... except TypeError: pass
    """
    obj1 = obj2[:]
    return obj1

def g(obj1, obj2, obj3, obj4):
    """
    >>> g(1, [1,2,3,4], 2, 3)
    [3, 4]
    >>> try: g(1, 42, 2, 3)
    ... except TypeError: pass
    """
    obj1 = obj2[obj3:]
    return obj1

def h(obj1, obj2, obj3, obj4):
    """
    >>> h(1, [1,2,3,4], 2, 3)
    [1, 2, 3]
    >>> try: h(1, 42, 2, 3)
    ... except TypeError: pass
    """
    obj1 = obj2[:obj4]
    return obj1

def j(obj1, obj2, obj3, obj4):
    """
    >>> j(1, [1,2,3,4], 2, 3)
    [3]
    >>> try: j(1, 42, 2, 3)
    ... except TypeError: pass
    """
    obj1 = obj2[obj3:obj4]
    return obj1

class A(object):
    pass

def slice_of_temporary_smoketest():
    """
    >>> slice_of_temporary_smoketest()
    [3, 2]
    """
    x = A()
    x.a = [1, 2]
    x.a[:] = [3,2]
    return x.a
