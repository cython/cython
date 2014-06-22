# Py2.7+ only

import sys


def test_set_literal():
    """
    >>> type(test_set_literal()) is set
    True
    >>> sorted(test_set_literal())
    ['a', 'b', 1]
    """
    s1 = {1, 'a', 1, 'b', 'a'}
    return s1


def test_set_add():
    """
    >>> type(test_set_add()) is set
    True
    >>> sorted(test_set_add())
    ['a', 1, (1, 2)]
    """
    s1 = {1, (1, 2)}
    s1.add(1)
    s1.add('a')
    s1.add(1)
    s1.add((1, 2))
    return s1


def test_set_comp():
    """
    >>> type(test_set_comp()) is set
    True
    >>> sorted(test_set_comp())
    [0, 1, 2]
    """
    s1 = {i % 3 for i in range(5)}
    return s1


def test_frozenset_set_comp():
    """
    >>> type(test_frozenset_set_comp()) is frozenset
    True
    >>> sorted(test_frozenset_set_comp())
    [0, 1, 2]
    """
    s1 = frozenset({i % 3 for i in range(5)})
    return s1


def test_set_sideeffect_unhashable_failure_literal():
    """
    >>> test_set_sideeffect_unhashable_failure_literal()
    [2, 4, 5]
    """
    L = []

    def sideeffect(x):
        L.append(x)
        return x

    def unhashable_value(x):
        L.append(x)
        return set()
    try:
        s = {1, sideeffect(2), 3, unhashable_value(4), sideeffect(5)}
    except TypeError: pass
    else: assert False, "expected exception not raised"
    return L


def test_set_comp_sideeffect_unhashable_failure():
    """
    >>> test_set_comp_sideeffect_unhashable_failure()
    (None, [2, 4])
    """
    L = []

    def value(x):
        return x

    def sideeffect(x):
        L.append(x)
        return x

    def unhashable_value(x):
        L.append(x)
        return set()
    s = None
    try:
        s = {f(i) for i, f in enumerate([value, sideeffect, value, unhashable_value, sideeffect], 1)}
    except TypeError: pass
    else: assert False, "expected exception not raised"
    return s, L


def sorted(it):
    # Py3 can't compare different types
    chars = []
    nums = []
    tuples = []
    for item in it:
        if type(item) is int:
            nums.append(item)
        elif type(item) is tuple:
            tuples.append(item)
        else:
            chars.append(item)
    nums.sort()
    chars.sort()
    tuples.sort()
    return chars+nums+tuples
