# mode: run
# tag: list, dict, setitem, delitem

def set_item(obj, key, value):
    """
    >>> set_item([1, 2, 3], 1, -1)
    [1, -1, 3]
    >>> set_item([1, 2, 3], -1, -1)
    [1, 2, -1]
    >>> set_item({}, 'abc', 5)
    {'abc': 5}
    >>> set_item({}, -1, 5)
    {-1: 5}
    >>> class D(dict): pass
    >>> set_item(D({}), 'abc', 5)
    {'abc': 5}
    >>> set_item(D({}), -1, 5)
    {-1: 5}
    """
    obj[key] = value
    return obj


def set_item_int(obj, int key, value):
    """
    >>> set_item_int([1, 2, 3], 1, -1)
    [1, -1, 3]
    >>> set_item_int([1, 2, 3], -1, -1)
    [1, 2, -1]
    >>> set_item_int({}, 1, 5)
    {1: 5}
    >>> set_item_int({}, -1, 5)
    {-1: 5}
    >>> class D(dict): pass
    >>> set_item_int(D({}), 1, 5)
    {1: 5}
    >>> set_item_int(D({}), -1, 5)
    {-1: 5}
    """
    obj[key] = value
    return obj


def del_item(obj, key):
    """
    >>> del_item([1, 2, 3], 1)
    [1, 3]
    >>> del_item([1, 2, 3], -3)
    [2, 3]
    >>> class D(dict): pass
    >>> del_item({'abc': 1, 'def': 2}, 'abc')
    {'def': 2}
    >>> del_item(D({'abc': 1, 'def': 2}), 'abc')
    {'def': 2}
    >>> del_item(D({-1: 1, -2: 2}), -1)
    {-2: 2}
    """
    del obj[key]
    return obj


def del_item_int(obj, int key):
    """
    >>> del_item_int([1, 2, 3], 1)
    [1, 3]
    >>> del_item_int([1, 2, 3], -3)
    [2, 3]
    >>> class D(dict): pass
    >>> del_item_int(D({-1: 1, 1: 2}), 1)
    {-1: 1}
    >>> del_item_int(D({-1: 1, -2: 2}), -1)
    {-2: 2}
    """
    del obj[key]
    return obj
