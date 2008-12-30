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
    >>> test_list_pop()
    (2, [1])
    >>> test_list_pop0()
    (1, [2])
    >>> test_list_pop_all()
    True
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

def test_list_pop():
    cdef list s1
    l1 = [1,2]
    two = l1.pop()
    return two, l1

def test_list_pop0():
    cdef list s1
    l1 = [1,2]
    one = l1.pop(0)
    return one, l1

def test_list_pop_all():
    cdef list s1
    l1 = [1,2]
    try:
        l1.pop()
        l1.pop(-1)
        l1.pop(0)
    except IndexError:
        return True
    return False
