# mode: run
# tag: set

cimport cython


@cython.test_assert_path_exists(
    "//SetIterationNextNode",
)
def set_iter_comp(set s):
    """
    >>> s = set([1, 2, 3])
    >>> sorted(set_iter_comp(s))
    [1, 2, 3]
    """
    return [x for x in s]


@cython.test_assert_path_exists(
    "//SetIterationNextNode",
)
def set_iter_comp_typed(set s):
    """
    >>> s = set([1, 2, 3])
    >>> sorted(set_iter_comp(s))
    [1, 2, 3]
    """
    cdef int x
    return [x for x in s]


@cython.test_assert_path_exists(
    "//SetIterationNextNode",
)
def frozenset_iter_comp(frozenset s):
    """
    >>> s = frozenset([1, 2, 3])
    >>> sorted(frozenset_iter_comp(s))
    [1, 2, 3]
    """
    return [x for x in s]


@cython.test_assert_path_exists(
    "//SetIterationNextNode",
)
def set_iter_comp_frozenset(set s):
    """
    >>> s = set([1, 2, 3])
    >>> sorted(set_iter_comp(s))
    [1, 2, 3]
    """
    return [x for x in frozenset(s)]


@cython.test_assert_path_exists(
    "//SetIterationNextNode",
)
def set_iter_modify(set s, int value):
    """
    >>> s = set([1, 2, 3])
    >>> sorted(set_iter_modify(s, 1))
    [1, 2, 3]
    >>> sorted(set_iter_modify(s, 2))
    [1, 2, 3]
    >>> sorted(set_iter_modify(s, 3))
    [1, 2, 3]
    >>> sorted(set_iter_modify(s, 4))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    RuntimeError: ...et changed size during iteration
    """
    for x in s:
        s.add(value)
    return s


@cython.test_fail_if_path_exists(
    "//SimpleCallNode//NameNode[@name = 'enumerate']",
)
@cython.test_assert_path_exists(
    "//AddNode",
    "//SetIterationNextNode",
)
def set_iter_enumerate(set s):
    """
    >>> s = set(['a', 'b', 'c'])
    >>> numbers, values = set_iter_enumerate(s)
    >>> sorted(numbers)
    [0, 1, 2]
    >>> sorted(values)
    ['a', 'b', 'c']
    """
    cdef int i
    numbers = []
    values = []
    for i, x in enumerate(s):
        numbers.append(i)
        values.append(x)
    return numbers, values
