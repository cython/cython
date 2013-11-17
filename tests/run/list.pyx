
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

def test_list_append_insert():
    """
    >>> test_list_append_insert()
    ['first', 'second']
    """
    cdef list l = []
    l.append("second")
    l.insert(0, "first")
    return l

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
    i = 0
    try:
        l1.pop()
        i = 1
        l1.pop(-1)
        i = 2
        l1.pop(0)
        i = 3
    except IndexError:
        return i == 2
    return False

def test_list_extend():
    """
    >>> test_list_extend()
    [1, 2, 3, 4, 5, 6]
    """
    cdef list l = [1,2,3]
    l.extend([])
    l.extend(())
    l.extend(set())
    assert l == [1,2,3]
    assert len(l) == 3
    l.extend([4,5,6])
    return l

def test_none_list_extend(list l):
    """
    >>> test_none_list_extend([])
    [1, 2, 3]
    >>> test_none_list_extend([0, 0, 0])
    [0, 0, 0, 1, 2, 3]
    >>> test_none_list_extend(None)
    123
    """
    try:
        l.extend([1,2,3])
    except AttributeError:
        return 123
    return l
