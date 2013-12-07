cimport cython

@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def str_startswith(str s, sub, start=None, stop=None):
    """
    >>> str_startswith('a', 'a')
    True
    >>> str_startswith('ab', 'a')
    True
    >>> str_startswith('a', 'b')
    False
    >>> str_startswith('ab', 'b')
    False
    >>> str_startswith('a', ('a', 'b'))
    True
    >>> str_startswith('a', 'a', 1)
    False
    >>> str_startswith('a', 'a', 0, 0)
    False
    """

    if start is None:
      return s.startswith(sub)
    elif stop is None:
      return s.startswith(sub, start)
    else:
      return s.startswith(sub, start, stop)

@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def str_endswith(str s, sub, start=None, stop=None):
    """
    >>> str_endswith('a', 'a')
    True
    >>> str_endswith('ba', 'a')
    True
    >>> str_endswith('a', 'b')
    False
    >>> str_endswith('ba', 'b')
    False
    >>> str_endswith('a', ('a', 'b'))
    True
    >>> str_endswith('a', 'a', 1)
    False
    >>> str_endswith('a', 'a', 0, 0)
    False
    """

    if start is None:
      return s.endswith(sub)
    elif stop is None:
      return s.endswith(sub, start)
    else:
      return s.endswith(sub, start, stop)


@cython.test_assert_path_exists(
    "//SimpleCallNode",
    "//SimpleCallNode//NoneCheckNode",
    "//SimpleCallNode//AttributeNode[@is_py_attr = false]")
def str_join(str s, args):
    """
    >>> print(str_join('a', list('bbb')))
    babab
    """
    result = s.join(args)
    assert cython.typeof(result) == 'basestring object', cython.typeof(result)
    return result


@cython.test_fail_if_path_exists(
    "//SimpleCallNode//NoneCheckNode",
)
@cython.test_assert_path_exists(
    "//SimpleCallNode",
    "//SimpleCallNode//AttributeNode[@is_py_attr = false]")
def literal_join(args):
    """
    >>> print(literal_join(list('abcdefg')))
    a|b|c|d|e|f|g
    """
    result = '|'.join(args)
    assert cython.typeof(result) == 'basestring object', cython.typeof(result)
    return result
