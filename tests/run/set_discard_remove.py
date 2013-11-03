
def set_discard():
    """
    >>> sorted(set_discard())
    [1, 2]
    """
    s = set([1,2,3])
    s.discard(3)
    return s


def set_discard_missing():
    """
    >>> sorted(set_discard_missing())
    [1, 2, 3]
    """
    s = set([1,2,3])
    s.discard(4)
    return s


def set_discard_set():
    """
    >>> s = set_discard_set()
    >>> len(s)
    1
    >>> sorted(s.pop())
    [1, 2]
    """
    s = set([frozenset([1,2]), frozenset([2,3])])
    s.discard(set([2,3]))
    return s


def set_remove():
    """
    >>> sorted(set_remove())
    [1, 2]
    """
    s = set([1,2,3])
    s.remove(3)
    return s


def set_remove_missing():
    """
    >>> sorted(set_remove_missing())
    Traceback (most recent call last):
    KeyError: 4
    """
    s = set([1,2,3])
    s.remove(4)
    return s


def set_remove_set():
    """
    >>> s = set_remove_set()
    >>> len(s)
    1
    >>> sorted(s.pop())
    [1, 2]
    """
    s = set([frozenset([1,2]), frozenset([2,3])])
    s.remove(set([2,3]))
    return s
