
cimport cython

def f(obj1, obj2, obj3, obj4, obj5):
    """
    >>> f(1, 2, 3, 4, 5)
    []
    """
    obj1 = []
    return obj1

def g(obj1, obj2, obj3, obj4, obj5):
    """
    >>> g(1, 2, 3, 4, 5)
    [2]
    """
    obj1 = [obj2]
    return obj1

def h(obj1, obj2, obj3, obj4, obj5):
    """
    >>> h(1, 2, 3, 4, 5)
    [2, 3]
    """
    obj1 = [obj2, obj3]
    return obj1

def j(obj1, obj2, obj3, obj4, obj5):
    """
    >>> j(1, 2, 3, 4, 5)
    [2, 3, 4]
    """
    obj1 = [obj2, obj3, obj4]
    return obj1

def k(obj1, obj2, obj3, obj4, obj5):
    """
    >>> k(1, 2, 3, 4, 5)
    [17, 42, 88]
    """
    obj1 = [17, 42, 88]
    return obj1

def test_list_sort():
    """
    >>> test_list_sort()
    [1, 2, 3, 4]
    """
    cdef list l1
    l1 = [2,3,1,4]
    l1.sort()
    return l1

def test_list_sort_reversed():
    cdef list l1
    l1 = [2,3,1,4]
    l1.sort(reversed=True)
    return l1

def test_list_reverse():
    """
    >>> test_list_reverse()
    [1, 2, 3, 4]
    """
    cdef list l1
    l1 = [4,3,2,1]
    l1.reverse()
    return l1

def test_list_append():
    """
    >>> test_list_append()
    [1, 2, 3, 4]
    """
    cdef list l1 = [1,2]
    l1.append(3)
    l1.append(4)
    return l1

def test_list_pop():
    """
    >>> test_list_pop()
    (2, [1])
    """
    cdef list l1
    l1 = [1,2]
    two = l1.pop()
    return two, l1

def test_list_pop0():
    """
    >>> test_list_pop0()
    (1, [2])
    """
    cdef list l1
    l1 = [1,2]
    one = l1.pop(0)
    return one, l1

def test_list_pop_all():
    """
    >>> test_list_pop_all()
    True
    """
    cdef list l1
    l1 = [1,2]
    try:
        l1.pop()
        l1.pop(-1)
        l1.pop(0)
    except IndexError:
        return True
    return False
