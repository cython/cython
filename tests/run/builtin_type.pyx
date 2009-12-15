cimport cython

@cython.test_assert_path_exists(
    '//PythonCapiCallNode/PythonCapiFunctionNode[@cname="Py_TYPE"]')
def get_type_of(a):
    """
    >>> get_type_of(object()) is object
    True
    """
    return type(a)

@cython.test_assert_path_exists(
    '//PythonCapiCallNode/PythonCapiFunctionNode[@cname="Py_TYPE"]')
def get_type_through_local(a):
    """
    >>> get_type_of(object()) is object
    True
    """
    t = type(a)
    return t

@cython.test_assert_path_exists(
    '//PythonCapiCallNode/PythonCapiFunctionNode[@cname="Py_TYPE"]')
@cython.test_fail_if_path_exists(
    '//PythonCapiCallNode/PythonCapiFunctionNode[@cname="__Pyx_Type"]',
    '//NameNode[@name="type"]')
def test_type(a, t):
    """
    >>> test_type(object(), object)
    True
    """
    return type(a) and type(a) is t and type(a) == t

@cython.test_assert_path_exists('//NameNode[@name="type"]')
def type_type():
    """
    >>> type_type()(object()) is object
    True
    """
    return type
