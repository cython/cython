# mode: run
# tag: builtins

cimport cython

@cython.test_assert_path_exists(
    '//ReturnStatNode//PythonCapiCallNode')
def unbound_dict_get(d):
    """
    >>> unbound_dict_get({})
    >>> unbound_dict_get({1:2})
    2
    """
    get = dict.get
    return get(d, 1)


@cython.test_assert_path_exists(
    '//ReturnStatNode//PythonCapiCallNode')
def bound_dict_get(dict d):
    """
    >>> bound_dict_get({})
    >>> bound_dict_get({1:2})
    2
    """
    get = d.get
    return get(1)


@cython.test_fail_if_path_exists(
    '//ReturnStatNode//PythonCapiCallNode')
@cython.test_assert_path_exists(
    '//ReturnStatNode//PyMethodCallNode')
def bound_dict_get_reassign(dict d):
    """
    >>> bound_dict_get_reassign({})
    >>> bound_dict_get_reassign({1:2})
    2
    """
    get = d.get
    d = {1: 3}
    return get(1)


@cython.test_assert_path_exists(
    '//PythonCapiCallNode//NameNode[@name="l"]')
def unbound_list_sort(list l):
    """
    >>> unbound_list_sort([1, 3, 2])
    [1, 2, 3]
    >>> unbound_list_sort([1, 3, 2])
    [1, 2, 3]
    """
    sort = list.sort
    sort(l)
    return l


@cython.test_assert_path_exists(
    '//PythonCapiCallNode//NameNode[@name="l"]')
def bound_list_sort(list l):
    """
    >>> bound_list_sort([1, 3, 2])
    [1, 2, 3]
    >>> bound_list_sort([1, 3, 2])
    [1, 2, 3]
    """
    sort = l.sort
    sort()
    return l


@cython.test_fail_if_path_exists(
    '//PythonCapiCallNode')
def bound_list_sort_reassign(list l):
    """
    >>> bound_list_sort_reassign([1, 3, 2])
    [3, 2, 1]
    >>> bound_list_sort_reassign([1, 3, 2])
    [3, 2, 1]
    """
    sort = l.sort
    l = [3, 2, 1]
    sort()
    return l

@cython.test_assert_path_exists(
    '//PythonCapiCallNode')
def append_optimized(probably_list):
    """
    >>> l = []
    >>> append_optimized(l)
    >>> l
    [1]
    """
    probably_list.append(1)

cdef class AppendBug:
    # https://github.com/cython/cython/issues/4828
    # if the attribute "append" is found it shouldn't be replaced with
    # __Pyx_PyObject_Append
    cdef object append
    def __init__(self, append):
        self.append = append

@cython.test_fail_if_path_exists(
    '//PythonCapiCallNode')
def specific_attribute(AppendBug a):
    """
    >>> def append_to_default_arg(a, arg=[]):
    ...    arg.append(a)
    ...    return arg
    >>> specific_attribute(AppendBug(append_to_default_arg))
    >>> append_to_default_arg(None)
    [1, None]
    """
    a.append(1)
