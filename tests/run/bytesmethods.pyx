cimport cython

b_a = b'a'
b_b = b'b'


@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
@cython.test_fail_if_path_exists(
    "//SimpleCallNode")
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
@cython.test_fail_if_path_exists(
    "//SimpleCallNode")
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


@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
@cython.test_fail_if_path_exists(
    "//SimpleCallNode")
def bytes_decode(bytes s, start=None, stop=None):
    """
    >>> s = b_a+b_b+b_a+b_a+b_b
    >>> print(bytes_decode(s))
    abaab

    >>> print(bytes_decode(s, 2))
    aab
    >>> print(bytes_decode(s, -3))
    aab

    >>> print(bytes_decode(s, None, 4))
    abaa
    >>> print(bytes_decode(s, None, 400))
    abaab
    >>> print(bytes_decode(s, None, -2))
    aba
    >>> print(bytes_decode(s, None, -4))
    a
    >>> print(bytes_decode(s, None, -5))
    <BLANKLINE>
    >>> print(bytes_decode(s, None, -200))
    <BLANKLINE>

    >>> print(bytes_decode(s, 2, 5))
    aab
    >>> print(bytes_decode(s, 2, 500))
    aab
    >>> print(bytes_decode(s, 2, -1))
    aa
    >>> print(bytes_decode(s, 2, -3))
    <BLANKLINE>
    >>> print(bytes_decode(s, 2, -300))
    <BLANKLINE>
    >>> print(bytes_decode(s, -3, -1))
    aa
    >>> print(bytes_decode(s, -300, 300))
    abaab
    >>> print(bytes_decode(s, -300, -4))
    a
    >>> print(bytes_decode(s, -300, -5))
    <BLANKLINE>
    >>> print(bytes_decode(s, -300, -6))
    <BLANKLINE>
    >>> print(bytes_decode(s, -300, -500))
    <BLANKLINE>

    >>> s[:'test']                       # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError:...
    >>> print(bytes_decode(s, 'test'))   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError:...
    >>> print(bytes_decode(s, None, 'test'))    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError:...
    >>> print(bytes_decode(s, 'test', 'test'))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError:...

    >>> print(bytes_decode(None))
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'decode'
    >>> print(bytes_decode(None, 1))
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    >>> print(bytes_decode(None, None, 1))
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    >>> print(bytes_decode(None, 0, 1))
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    """
    if start is None:
        if stop is None:
            return s.decode('utf8')
        else:
            return s[:stop].decode('utf8')
    elif stop is None:
        return s[start:].decode('utf8')
    else:
        return s[start:stop].decode('utf8')


@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
@cython.test_fail_if_path_exists(
    "//SimpleCallNode")
def bytes_decode_utf16(bytes s):
    """
    >>> s = 'abc'.encode('UTF-16')
    >>> print(bytes_decode_utf16(s))
    abc
    """
    return s.decode('utf16')


@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
@cython.test_fail_if_path_exists(
    "//SimpleCallNode")
def bytes_decode_utf16_le(bytes s):
    """
    >>> s = 'abc'.encode('UTF-16LE')
    >>> assert s != 'abc'.encode('UTF-16BE')
    >>> print(bytes_decode_utf16_le(s))
    abc
    """
    return s.decode('utf_16_le')


@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
@cython.test_fail_if_path_exists(
    "//SimpleCallNode")
def bytes_decode_utf16_be(bytes s):
    """
    >>> s = 'abc'.encode('UTF-16BE')
    >>> assert s != 'abc'.encode('UTF-16LE')
    >>> print(bytes_decode_utf16_be(s))
    abc
    """
    return s.decode('utf_16_be')


@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
@cython.test_fail_if_path_exists(
    "//SimpleCallNode")
def bytes_decode_unbound_method(bytes s, start=None, stop=None):
    """
    >>> s = b_a+b_b+b_a+b_a+b_b
    >>> print(bytes_decode_unbound_method(s))
    abaab
    >>> print(bytes_decode_unbound_method(s, 1))
    baab
    >>> print(bytes_decode_unbound_method(s, None, 3))
    aba
    >>> print(bytes_decode_unbound_method(s, 1, 4))
    baa

    >>> print(bytes_decode_unbound_method(None))
    Traceback (most recent call last):
    TypeError: descriptor 'decode' requires a 'bytes' object but received a 'NoneType'
    >>> print(bytes_decode_unbound_method(None, 1))
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    >>> print(bytes_decode_unbound_method(None, None, 1))
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    >>> print(bytes_decode_unbound_method(None, 0, 1))
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    """
    if start is None:
        if stop is None:
            return bytes.decode(s, 'utf8')
        else:
            return bytes.decode(s[:stop], 'utf8')
    elif stop is None:
        return bytes.decode(s[start:], 'utf8')
    else:
        return bytes.decode(s[start:stop], 'utf8')


@cython.test_assert_path_exists(
    "//SimpleCallNode",
    "//SimpleCallNode//NoneCheckNode",
    "//SimpleCallNode//AttributeNode[@is_py_attr = false]")
def bytes_join(bytes s, *args):
    """
    >>> print(bytes_join(b_a, b_b, b_b, b_b).decode('utf8'))
    babab
    """
    result = s.join(args)
    assert cython.typeof(result) == 'Python object', cython.typeof(result)
    return result


@cython.test_fail_if_path_exists(
    "//SimpleCallNode//NoneCheckNode",
)
@cython.test_assert_path_exists(
    "//SimpleCallNode",
    "//SimpleCallNode//AttributeNode[@is_py_attr = false]")
def literal_join(*args):
    """
    >>> print(literal_join(b_b, b_b, b_b, b_b).decode('utf8'))
    b|b|b|b
    """
    result = b'|'.join(args)
    assert cython.typeof(result) == 'Python object', cython.typeof(result)
    return result
