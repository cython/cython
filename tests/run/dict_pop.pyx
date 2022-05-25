# mode: run
# tag: dict, pop, builtins

cimport cython

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def dict_pop(dict d, key):
    """
    >>> d = { 1: 10, 2: 20 }
    >>> dict_pop(d, 1)
    (10, {2: 20})
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
    >>> dict_pop_default(d, 3, None)
    (None, {2: 20})
    >>> dict_pop_default(d, 3, "default")
    ('default', {2: 20})
    >>> dict_pop_default(d, 2, "default")
    (20, {})
    """
    return d.pop(key, default), d


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
