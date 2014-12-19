
def list_insert(list l):
    """
    >>> list_insert([1,2,3])
    [1, 4, 2, 3]
    """
    list.insert(l, 1, 4)
    return l


def list_insert_literal():
    """
    >>> list_insert_literal()
    (None, [1, 4, 2, 3])
    """
    l = [1,2,3]
    r = list.insert(l, 1, 4)
    return r, l


def list_insert_assigned():
    """
    >>> list_insert_assigned()
    (None, [1, 4, 2, 3])
    """
    insert = list.insert
    l = [1,2,3]
    r = insert(l, 1, 4)
    return r, l


def list_pop():
    """
    >>> list_pop()
    (2, [1, 3])
    """
    l = [1,2,3]
    r = list.pop(l, 1)
    return r, l


def list_pop_assigned():
    """
    >>> list_pop_assigned()
    [1, 3]
    """
    pop = list.pop
    l = [1,2,3]
    pop(l, 1)
    return l
