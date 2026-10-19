# mode: run
# tag: dict, pop, builtins

cimport cython


def make_frozendict(d):
    return frozendict(d)


class FailHash:
    def __hash__(self):
        raise TypeError()


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def dict_pop(dict d, key):
    """
    >>> d = { 1: 10, 2: 20 }
    >>> dict_pop(d, 1)
    (10, {2: 20})
    >>> dict_pop(d, FailHash())  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError
    >>> d
    {2: 20}
    >>> dict_pop(d, 3)
    Traceback (most recent call last):
    KeyError: 3
    >>> dict_pop(d, 2)
    (20, {})
    """
    return d.pop(key), d


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def dict_pop_default(dict d, key, default):
    """
    >>> d = { 1: 10, 2: 20 }
    >>> dict_pop_default(d, 1, "default")
    (10, {2: 20})
    >>> dict_pop_default(d, FailHash(), 30)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError
    >>> d
    {2: 20}
    >>> dict_pop_default(d, 3, None)
    (None, {2: 20})
    >>> dict_pop_default(d, 3, "default")
    ('default', {2: 20})
    >>> dict_pop_default(d, 2, "default")
    (20, {})
    """
    return d.pop(key, default), d


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def dict_pop_ignored(dict d, key):
    """
    >>> d = {1: 2, 'a': 'b'}
    >>> dict_pop_ignored(d, 'a')
    >>> d
    {1: 2}
    >>> dict_pop_ignored(d, FailHash())  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError
    >>> d
    {1: 2}
    >>> dict_pop_ignored(d, 123)
    >>> d
    {1: 2}
    """
    d.pop(key, None)


cdef class MyType:
    cdef public int i
    def __init__(self, i):
        self.i = i


@cython.test_assert_path_exists("//SingleAssignmentNode//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//SingleAssignmentNode//AttributeNode")
def dict_pop_default_typed(dict d, key, default):
    """
    >>> d = {1: MyType(2)}
    >>> dict_pop_default_typed(d, 1, None)
    2
    >>> dict_pop_default_typed(d, 3, None)
    >>> dict_pop_default_typed(d, 3, "default")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: Cannot convert str to ...MyType
    """
    cdef MyType x = d.pop(key, default)
    return x.i if x is not None else None


def pop_frozendict(frozendict fd, key):
    """
    Confirms that frozendict has no `pop` method (deliberately not aliased
    in the compiler-side method-handler dispatch — frozendict is immutable).
    On Python <3.15, `frozendict` falls back to plain `dict` which DOES have
    `pop`, so we only assert the raise on supported Pythons.

    >>> import sys
    >>> if sys.version_info >= (3, 15, 0, 'alpha', 7):
    ...     try: pop_frozendict(make_frozendict({1: 10}), 1)
    ...     except AttributeError: print("AttributeError")
    ...     else: print("no error")
    ... else:
    ...     print("AttributeError")
    AttributeError
    """
    return fd.pop(key)


def return_pop_typed_dict(d: dict[str,int], key: str):
    """
    >>> d = {'1': 2, 'a': 4}
    >>> return_pop_typed_dict(d, '1')
    2
    >>> d
    {'a': 4}
    """
    return d.pop(key)


def return_pop_typed_dict_default(d: dict[str,int], key: str, default: int):
    """
    >>> d = {'1': 2, 'a': 4}
    >>> return_pop_typed_dict_default(d, '1', 3)
    2
    >>> return_pop_typed_dict_default(d, '1', 3)
    3
    >>> return_pop_typed_dict_default(d, '1', 3)
    3
    """
    return d.pop(key, default)


def pop_typed_dict_ignored(d: dict[str,int], key: str):
    """
    >>> d = {'1': 2, 'a': 4}
    >>> pop_typed_dict_ignored(d, '1')
    >>> d
    {'a': 4}
    """
    d.pop(key)


def pop_typed_dict_ignored_default(d: dict[str,int], key: str, default: int):
    """
    >>> d = {'1': 2, 'a': 4}
    >>> pop_typed_dict_ignored_default(d, '2', 3)
    >>> d
    {'1': 2, 'a': 4}
    >>> pop_typed_dict_ignored_default(d, '1', 3)
    >>> d
    {'a': 4}
    >>> pop_typed_dict_ignored_default(d, '1', 3)
    >>> d
    {'a': 4}
    """
    d.pop(key, default)


def pop_typed_dict_wrong_cast(d: dict[str,int], key: str):
    """
    >>> d = {'1': 2, 'a': 4}
    >>> pop_typed_dict_wrong_cast(d, '1')
    Traceback (most recent call last):
    TypeError: Expected list, got int
    """
    <list?> d.pop(key)  # incorrect cast should fail
