
def f(obj1, obj2, obj3, obj4, obj5):
    """
    >>> f(1,2,3,4,5)
    ()
    """
    obj1 = ()
    return obj1

def g(obj1, obj2, obj3, obj4, obj5):
    """
    >>> g(1,2,3,4,5)
    (2,)
    """
    obj1 = ()
    obj1 = (obj2,)
    return obj1

def h(obj1, obj2, obj3, obj4, obj5):
    """
    >>> h(1,2,3,4,5)
    (2, 3)
    """
    obj1 = ()
    obj1 = (obj2,)
    obj1 = obj2, obj3
    return obj1

def j(obj1, obj2, obj3, obj4, obj5):
    """
    >>> j(1,2,3,4,5)
    (2, 3, 4)
    """
    obj1 = ()
    obj1 = (obj2,)
    obj1 = obj2, obj3
    obj1 = (obj2, obj3, obj4)
    return obj1

def k(obj1, obj2, obj3, obj4, obj5):
    """
    >>> k(1,2,3,4,5)
    (2, 3, 4)
    """
    obj1 = ()
    obj1 = (obj2,)
    obj1 = obj2, obj3
    obj1 = (obj2, obj3, obj4)
    obj1 = (obj2, obj3, obj4,)
    return obj1

def l(obj1, obj2, obj3, obj4, obj5):
    """
    >>> l(1,2,3,4,5)
    (17, 42, 88)
    """
    obj1 = ()
    obj1 = (obj2,)
    obj1 = obj2, obj3
    obj1 = (obj2, obj3, obj4)
    obj1 = (obj2, obj3, obj4,)
    obj1 = 17, 42, 88
    return obj1

def tuple_none():
    """
    >>> tuple_none()   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...itera...
    """
    return tuple(None)

def tuple_none_list():
    """
    >>> tuple_none_list()   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...iterable...
    """
    cdef list none = None
    return tuple(none)
