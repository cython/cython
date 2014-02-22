
# Py2.3 doesn't have the 'set' builtin type, but Cython does :)
_set = set
_frozenset = frozenset

cimport cython

import sys


def cython_set():
    """
    >>> cython_set() is _set
    True
    """
    assert set is cython.set
    return cython.set


def cython_frozenset():
    """
    >>> cython_frozenset() is _frozenset
    True
    """
    assert frozenset is cython.frozenset
    return cython.frozenset


def cython_set_override():
    """
    >>> cython_set_override() is _set
    True
    """
    set = 1
    return cython.set


def cython_frozenset_override():
    """
    >>> cython_frozenset_override() is _frozenset
    True
    """
    frozenset = 1
    return cython.frozenset


def test_set_literal():
    """
    >>> type(test_set_literal()) is _set
    True
    >>> sorted(test_set_literal())
    ['a', 'b', 1]
    """
    cdef set s1 = {1,'a',1,'b','a'}
    return s1


def test_set_add():
    """
    >>> type(test_set_add()) is _set
    True
    >>> sorted(test_set_add())
    ['a', 1, (1, 2)]
    """
    cdef set s1
    s1 = set([1, (1, 2)])
    s1.add(1)
    s1.add('a')
    s1.add(1)
    s1.add((1,2))
    return s1


def test_set_clear():
    """
    >>> type(test_set_clear()) is _set
    True
    >>> list(test_set_clear())
    []
    """
    cdef set s1
    s1 = set([1])
    s1.clear()
    return s1


def test_set_clear_None():
    """
    >>> test_set_clear_None()
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'clear'
    """
    cdef set s1 = None
    s1.clear()


def test_set_list_comp():
    """
    >>> type(test_set_list_comp()) is _set
    True
    >>> sorted(test_set_list_comp())
    [0, 1, 2]
    """
    cdef set s1
    s1 = set([i%3 for i in range(5)])
    return s1


def test_frozenset_list_comp():
    """
    >>> type(test_frozenset_list_comp()) is _frozenset
    True
    >>> sorted(test_frozenset_list_comp())
    [0, 1, 2]
    """
    cdef frozenset s1
    s1 = frozenset([i%3 for i in range(5)])
    return s1


def test_set_pop():
    """
    >>> type(test_set_pop()) is _set
    True
    >>> list(test_set_pop())
    []
    """
    cdef set s1
    s1 = set()
    s1.add('2')
    two = s1.pop()
    return s1


@cython.test_fail_if_path_exists("//SimpleCallNode//NameNode")
def test_object_pop(s):
    """
    >>> s = _set([2])
    >>> test_object_pop(s)
    2
    >>> list(s)
    []
    """
    return s.pop()


def test_set_discard():
    """
    >>> type(test_set_discard()) is _set
    True
    >>> sorted(test_set_discard())
    ['12', 233]
    """
    cdef set s1
    s1 = set()
    s1.add('12')
    s1.add(3)
    s1.add(233)
    s1.discard('3')
    s1.discard(3)
    return s1


def test_set_sideeffect_unhashable_failure():
    """
    >>> test_set_sideeffect_unhashable_failure()
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
        s = set([1,sideeffect(2),3,unhashable_value(4),sideeffect(5)])
    except TypeError: pass
    else: assert False, "expected exception not raised"
    return L


def test_frozenset_sideeffect_unhashable_failure():
    """
    >>> test_frozenset_sideeffect_unhashable_failure()
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
        s = frozenset([1,sideeffect(2),3,unhashable_value(4),sideeffect(5)])
    except TypeError: pass
    else: assert False, "expected exception not raised"
    return L


@cython.test_assert_path_exists("//SetNode")
@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//PythonCapiCallNode"
)
def test_set_of_list():
    """
    >>> s = test_set_of_list()
    >>> isinstance(s, _set)
    True
    >>> sorted(s)
    [1, 2, 3]
    """
    return set([1, 2, 3])


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//SetNode")
def test_frozenset_of_list():
    """
    >>> s = test_frozenset_of_list()
    >>> isinstance(s, _frozenset)
    True
    >>> sorted(s)
    [1, 2, 3]
    """
    return frozenset([1, 2, 3])


@cython.test_assert_path_exists("//SetNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def test_set_of_tuple():
    """
    >>> s = test_set_of_tuple()
    >>> isinstance(s, _set)
    True
    >>> sorted(s)
    [1, 2, 3]
    """
    return set((1, 2, 3))


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//SetNode")
def test_frozenset_of_tuple():
    """
    >>> s = test_frozenset_of_tuple()
    >>> isinstance(s, _frozenset)
    True
    >>> sorted(s)
    [1, 2, 3]
    """
    return frozenset((1, 2, 3))


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//SetNode"
)
def test_set_of_iterable(x):
    """
    >>> s = test_set_of_iterable([1, 2, 3])
    >>> isinstance(s, _set)
    True
    >>> sorted(s)
    [1, 2, 3]
    """
    return set(x)


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//SetNode"
)
def test_frozenset_of_iterable(x):
    """
    >>> s = test_frozenset_of_iterable([1, 2, 3])
    >>> isinstance(s, _frozenset)
    True
    >>> sorted(s)
    [1, 2, 3]

    >>> s = test_frozenset_of_iterable(_frozenset([1, 2, 3]))
    >>> isinstance(s, _frozenset)
    True
    >>> sorted(s)
    [1, 2, 3]
    """
    return frozenset(x)


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//SetNode"
)
def test_empty_frozenset():
    """
    >>> s = test_empty_frozenset()
    >>> isinstance(s, _frozenset)
    True
    >>> len(s)
    0
    >>> sys.version_info < (2,5) or s is frozenset()   # singleton!
    True
    """
    return frozenset()


@cython.test_fail_if_path_exists(
    '//ListNode//ListNode',
    '//ListNode//PythonCapiCallNode//PythonCapiCallNode',
    '//ListNode//SimpleCallNode//SimpleCallNode',
)
def test_singleton_empty_frozenset():
    """
    >>> test_singleton_empty_frozenset()  # from CPython's test_set.py
    1
    """
    f = frozenset()
    efs = [frozenset(), frozenset([]), frozenset(()), frozenset(''),
           frozenset(), frozenset([]), frozenset(()), frozenset(''),
           frozenset(range(0)), frozenset(frozenset()),
           frozenset(f), f]
    return len(set(map(id, efs))) if sys.version_info >= (2,5) else 1


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
