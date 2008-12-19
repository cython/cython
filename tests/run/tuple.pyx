__doc__ = u"""
    >>> f(1,2,3,4,5)
    ()
    >>> g(1,2,3,4,5)
    (2,)
    >>> h(1,2,3,4,5)
    (2, 3)
    >>> j(1,2,3,4,5)
    (2, 3, 4)
    >>> k(1,2,3,4,5)
    (2, 3, 4)
    >>> l(1,2,3,4,5)
    (17, 42, 88)
    >>> tuple_none()
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not iterable
    >>> tuple_none_list()
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not iterable
"""

def f(obj1, obj2, obj3, obj4, obj5):
    obj1 = ()
    return obj1

def g(obj1, obj2, obj3, obj4, obj5):
    obj1 = ()
    obj1 = (obj2,)
    return obj1

def h(obj1, obj2, obj3, obj4, obj5):
    obj1 = ()
    obj1 = (obj2,)
    obj1 = obj2, obj3
    return obj1

def j(obj1, obj2, obj3, obj4, obj5):
    obj1 = ()
    obj1 = (obj2,)
    obj1 = obj2, obj3
    obj1 = (obj2, obj3, obj4)
    return obj1

def k(obj1, obj2, obj3, obj4, obj5):
    obj1 = ()
    obj1 = (obj2,)
    obj1 = obj2, obj3
    obj1 = (obj2, obj3, obj4)
    obj1 = (obj2, obj3, obj4,)
    return obj1

def l(obj1, obj2, obj3, obj4, obj5):
    obj1 = ()
    obj1 = (obj2,)
    obj1 = obj2, obj3
    obj1 = (obj2, obj3, obj4)
    obj1 = (obj2, obj3, obj4,)
    obj1 = 17, 42, 88
    return obj1

def tuple_none():
    return tuple(None)

def tuple_none_list():
    cdef list none = None
    return tuple(none)
