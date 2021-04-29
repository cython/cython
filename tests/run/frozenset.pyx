# mode: run

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


def cython_frozenset_override():
    """
    >>> cython_frozenset_override() is frozenset
    True
    """
    frozenset = 1
    return cython.frozenset


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


@cython.test_fail_if_path_exists("//SetNode", "//PythonCapiCallNode")
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


@cython.test_fail_if_path_exists("//SetNode", "//PythonCapiCallNode")
def test_frozenset_of_tuple():
    """
    >>> s = test_frozenset_of_tuple()
    >>> isinstance(s, frozenset)
    True
    >>> sorted(s)
    [1, 2, 3]
    """
    return frozenset((1, 2, 3))





@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//SetNode",
    "//PythonCapiCallNode"
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


# def test_create_frozenset_from_string():
#     """
#     >>> s = test_create_frozenset_from_string()
#     >>> isinstance(s, frozenset)
#     True
#     >>> sorted(s)
#     ["1", "2", "3"]
#     """
#     return frozenset("1231")



# @cython.test_fail_if_path_exists(
#     "//SimpleCallNode",
#     "//SetNode",
#     "//PythonCapiCallNode"
# )
# def test_empty_frozenset():
#     """
#     >>> s = test_empty_frozenset()
#     >>> isinstance(s, frozenset)
#     True
#     >>> len(s)
#     0
#     >>> import sys
#     >>> sys.version_info >= (3, 10) or s is frozenset()   # singleton (in Python < 3.10)!
#     True
#     """
#     return frozenset()

# #TODO for next test
# def test_singleton_empty_frozenset():
#     """
#     >>> import sys
#     >>> test_singleton_empty_frozenset() if sys.version_info < (3, 10) else 1  # from CPython's test_set.py
#     1
#     """
#     f = frozenset()
#     efs = [frozenset(), frozenset([]), frozenset(()),
#            frozenset(), frozenset([]), frozenset(()),
#            frozenset(range(0)), frozenset(frozenset()),
#            frozenset(f), f]
#     return len(set(map(id, efs)))  # note, only a singleton in Python <3.10
#

# @cython.test_fail_if_path_exists(
#     '//ListNode//ListNode',
#     '//ListNode//PythonCapiCallNode//PythonCapiCallNode',
#     '//ListNode//SimpleCallNode//SimpleCallNode',
# )
# def test_singleton_empty_frozenset():
#     """
#     >>> import sys
#     >>> test_singleton_empty_frozenset() if sys.version_info < (3, 10) else 1  # from CPython's test_set.py
#     1
#     """
#     f = frozenset()
#     efs = [frozenset(), frozenset([]), frozenset(()), frozenset(''),
#            frozenset(), frozenset([]), frozenset(()), frozenset(''),
#            frozenset(range(0)), frozenset(frozenset()),
#            frozenset(f), f]
#     return len(set(map(id, efs)))  # note, only a singleton in Python <3.10


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
