def f(obj1, obj2, obj3, obj4, obj5):
    """
    >>> f(1, (2,), (3,4,5), (6,(7,(8,9))), 0)
    (8, 9, (8, 9), (6, (7, (8, 9))), 0)
    """
    obj1, = obj2
    obj1, obj2 = obj2 + obj2
    obj1, obj2, obj3 = obj3
    obj1, (obj2, obj3) = obj4
    [obj1, obj2] = obj3
    return obj1, obj2, obj3, obj4, obj5
