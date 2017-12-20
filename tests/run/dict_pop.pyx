
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
