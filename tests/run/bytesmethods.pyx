cimport cython

b_a = b'a'
b_b = b'b'

@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def bytes_startswith(bytes s, sub, start=None, stop=None):
    """
    >>> bytes_startswith(b_a, b_a)
    True
    >>> bytes_startswith(b_a+b_b, b_a)
    True
    >>> bytes_startswith(b_a, b_b)
    False
    >>> bytes_startswith(b_a+b_b, b_b)
    False
    >>> bytes_startswith(b_a, (b_a, b_b))
    True
    >>> bytes_startswith(b_a, b_a, 1)
    False
    >>> bytes_startswith(b_a, b_a, 0, 0)
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
    >>> bytes_endswith(b_a, b_a)
    True
    >>> bytes_endswith(b_b+b_a, b_a)
    True
    >>> bytes_endswith(b_a, b_b)
    False
    >>> bytes_endswith(b_b+b_a, b_b)
    False
    >>> bytes_endswith(b_a, (b_a, b_b))
    True
    >>> bytes_endswith(b_a, b_a, 1)
    False
    >>> bytes_endswith(b_a, b_a, 0, 0)
    False
    """

    if start is None:
      return s.endswith(sub)
    elif stop is None:
      return s.endswith(sub, start)
    else:
      return s.endswith(sub, start, stop)
