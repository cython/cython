
cimport cython


def cython_set():
    """
    >>> cython_set() is set
    True
    """
    assert set is cython.set
    return cython.set


def cython_frozenset():
    """
    >>> cython_frozenset() is frozenset
    True
    """
    assert frozenset is cython.frozenset
    return cython.frozenset


def cython_set_override():
    """
    >>> cython_set_override() is set
    True
    """
    set = 1
    return cython.set


def cython_frozenset_override():
    """
    >>> cython_frozenset_override() is frozenset
    True
    """
    frozenset = 1
    return cython.frozenset


def test_set_literal():
    """
    >>> type(test_set_literal()) is set
    True
    >>> sorted(test_set_literal())
    ['a', 'b', 1]
    """
    cdef set s1 = {1,'a',1,'b','a'}
    return s1


def test_set_add():
    """
    >>> type(test_set_add()) is set
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


def test_set_contains(v):
    """
    >>> test_set_contains(1)
    True
    >>> test_set_contains(2)
    False
    >>> test_set_contains(frozenset([1, 2, 3]))
    True
    >>> test_set_contains(frozenset([1, 2]))
    False
    >>> test_set_contains(set([1, 2, 3]))
    True
    >>> test_set_contains(set([1, 2]))
    False
    >>> try: test_set_contains([1, 2])
    ... except TypeError: pass
    ... else: print("NOT RAISED!")
    """
    cdef set s1
    s1 = set()
    s1.add(1)
    s1.add('a')
    s1.add(frozenset([1, 2, 3]))
    return v in s1


def test_set_update(v=None):
    """
    >>> type(test_set_update()) is set
    True
    >>> sorted(test_set_update())
    ['a', 'b', 'c', 1, 2, (1, 2)]
    >>> sorted(test_set_update([]))
    ['a', 'b', 'c', 1, 2, (1, 2)]
    >>> try: test_set_update(object())
    ... except TypeError: pass
    ... else: print("NOT RAISED!")
    """
    cdef set s1
    s1 = set([1, (1, 2)])
    s1.update((1,))
    s1.update('abc')
    s1.update(set([1]))
    s1.update(frozenset((1,2)))
    if v is not None:
        s1.update(v)
    return s1


def test_set_multi_update():
    """
    >>> type(test_set_multi_update()) is set
    True
    >>> sorted(test_set_multi_update())
    ['a', 'b', 'c', 1, 2, 3]
    """
    cdef set s1 = set()
    s1.update('abc', set([1, 3]), frozenset([1, 2]))
    return s1


def test_object_update(v=None):
    """
    >>> type(test_object_update()) is set
    True
    >>> sorted(test_object_update())
    ['a', 'b', 'c', 1, 2, (1, 2)]
    >>> sorted(test_object_update([]))
    ['a', 'b', 'c', 1, 2, (1, 2)]
    >>> try: test_object_update(object())
    ... except TypeError: pass
    ... else: print("NOT RAISED!")
    """
    cdef object s1
    s1 = set([1, (1, 2)])
    s1.update((1,))
    s1.update('abc')
    s1.update(set([1]))
    s1.update(frozenset((1,2)))
    if v is not None:
        s1.update(v)
    return s1


def test_set_clear():
    """
    >>> type(test_set_clear()) is set
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
    >>> type(test_set_list_comp()) is set
    True
    >>> sorted(test_set_list_comp())
    [0, 1, 2]
    """
    cdef set s1
    s1 = set([i%3 for i in range(5)])
    return s1


def test_frozenset_list_comp():
    """
    >>> type(test_frozenset_list_comp()) is frozenset
    True
    >>> sorted(test_frozenset_list_comp())
    [0, 1, 2]
    """
    cdef frozenset s1
    s1 = frozenset([i%3 for i in range(5)])
    return s1


def test_set_pop():
    """
    >>> type(test_set_pop()) is set
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
    >>> s = set([2])
    >>> test_object_pop(s)
    2
    >>> list(s)
    []
    """
    return s.pop()


def test_noop_pop():
    """
    >>> test_noop_pop()
    """
    set([0]).pop()


def test_noop_pop_exception():
    """
    >>> try: test_noop_pop_exception()
    ... except KeyError: pass
    ... else: print("KeyError expected but not raised!")
    """
    set([]).pop()


def test_set_discard():
    """
    >>> type(test_set_discard()) is set
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
        s = {1,sideeffect(2),3,unhashable_value(4),sideeffect(5)}
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
    >>> isinstance(s, set)
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
    >>> isinstance(s, frozenset)
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
    >>> isinstance(s, set)
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
    >>> isinstance(s, frozenset)
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
    >>> isinstance(s, set)
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
    >>> isinstance(s, frozenset)
    True
    >>> sorted(s)
    [1, 2, 3]

    >>> s = test_frozenset_of_iterable(frozenset([1, 2, 3]))
    >>> isinstance(s, frozenset)
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
    >>> isinstance(s, frozenset)
    True
    >>> len(s)
    0
    >>> import sys
    >>> sys.version_info >= (3, 10) or s is frozenset()   # singleton (in Python < 3.10)!
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
    >>> import sys
    >>> test_singleton_empty_frozenset() if sys.version_info < (3, 10) else 1  # from CPython's test_set.py
    1
    """
    f = frozenset()
    efs = [frozenset(), frozenset([]), frozenset(()), frozenset(''),
           frozenset(), frozenset([]), frozenset(()), frozenset(''),
           frozenset(range(0)), frozenset(frozenset()),
           frozenset(f), f]
    return len(set(map(id, efs)))  # note, only a singleton in Python <3.10


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
