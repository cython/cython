cimport cython

@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def bytes_startswith(bytes s, sub, start=None, stop=None):
    """
    >>> bytes_startswith(b'a', b'a')
    True
    >>> bytes_startswith(b'a', b'b')
    False
    >>> bytes_startswith(b'a', (b'a', b'b'))
    True
    >>> bytes_startswith(b'a', b'a', 1)
    False
    >>> bytes_startswith(b'a', b'a', 0, 0)
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
def bytes_endswith(bytes s, sub, start=None, stop=None):
    """
    >>> bytes_endswith(b'a', b'a')
    True
    >>> bytes_endswith(b'a', b'b')
    False
    >>> bytes_endswith(b'a', (b'a', b'b'))
    True
    >>> bytes_endswith(b'a', b'a', 1)
    False
    >>> bytes_endswith(b'a', b'a', 0, 0)
    False
    """

    if start is None:
      return s.endswith(sub)
    elif stop is None:
      return s.endswith(sub, start)
    else:
      return s.endswith(sub, start, stop)
