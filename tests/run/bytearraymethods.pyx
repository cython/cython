
cimport cython

b_a = bytearray(b'a')
b_b = bytearray(b'b')


'''   # disabled for now, enable when we consider it worth the code overhead

@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
@cython.test_fail_if_path_exists(
    "//SimpleCallNode")
def bytearray_startswith(bytearray s, sub, start=None, stop=None):
    """
    >>> bytearray_startswith(b_a, b_a)
    True
    >>> bytearray_startswith(b_a+b_b, b_a)
    True
    >>> bytearray_startswith(b_a, b_b)
    False
    >>> bytearray_startswith(b_a+b_b, b_b)
    False
    >>> bytearray_startswith(b_a, (b_a, b_b))
    True
    >>> bytearray_startswith(b_a, b_a, 1)
    False
    >>> bytearray_startswith(b_a, b_a, 0, 0)
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
def bytearray_endswith(bytearray s, sub, start=None, stop=None):
    """
    >>> bytearray_endswith(b_a, b_a)
    True
    >>> bytearray_endswith(b_b+b_a, b_a)
    True
    >>> bytearray_endswith(b_a, b_b)
    False
    >>> bytearray_endswith(b_b+b_a, b_b)
    False
    >>> bytearray_endswith(b_a, (b_a, b_b))
    True
    >>> bytearray_endswith(b_a, b_a, 1)
    False
    >>> bytearray_endswith(b_a, b_a, 0, 0)
    False
    """

    if start is None:
      return s.endswith(sub)
    elif stop is None:
      return s.endswith(sub, start)
    else:
      return s.endswith(sub, start, stop)
'''


@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
@cython.test_fail_if_path_exists(
    "//SimpleCallNode")
def bytearray_decode(bytearray s, start=None, stop=None):
    """
    >>> s = b_a+b_b+b_a+b_a+b_b
    >>> print(bytearray_decode(s))
    abaab

    >>> print(bytearray_decode(s, 2))
    aab
    >>> print(bytearray_decode(s, -3))
    aab

    >>> print(bytearray_decode(s, None, 4))
    abaa
    >>> print(bytearray_decode(s, None, 400))
    abaab
    >>> print(bytearray_decode(s, None, -2))
    aba
    >>> print(bytearray_decode(s, None, -4))
    a
    >>> print(bytearray_decode(s, None, -5))
    <BLANKLINE>
    >>> print(bytearray_decode(s, None, -200))
    <BLANKLINE>

    >>> print(bytearray_decode(s, 2, 5))
    aab
    >>> print(bytearray_decode(s, 2, 500))
    aab
    >>> print(bytearray_decode(s, 2, -1))
    aa
    >>> print(bytearray_decode(s, 2, -3))
    <BLANKLINE>
    >>> print(bytearray_decode(s, 2, -300))
    <BLANKLINE>
    >>> print(bytearray_decode(s, -3, -1))
    aa
    >>> print(bytearray_decode(s, -300, 300))
    abaab
    >>> print(bytearray_decode(s, -300, -4))
    a
    >>> print(bytearray_decode(s, -300, -5))
    <BLANKLINE>
    >>> print(bytearray_decode(s, -300, -6))
    <BLANKLINE>
    >>> print(bytearray_decode(s, -300, -500))
    <BLANKLINE>

    >>> s[:'test']                       # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError:...
    >>> print(bytearray_decode(s, 'test'))   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError:...
    >>> print(bytearray_decode(s, None, 'test'))    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError:...
    >>> print(bytearray_decode(s, 'test', 'test'))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError:...

    >>> print(bytearray_decode(None))
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'decode'
    >>> print(bytearray_decode(None, 1))
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    >>> print(bytearray_decode(None, None, 1))
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    >>> print(bytearray_decode(None, 0, 1))
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
def bytearray_decode_unbound_method(bytearray s, start=None, stop=None):
    """
    >>> s = b_a+b_b+b_a+b_a+b_b
    >>> print(bytearray_decode_unbound_method(s))
    abaab
    >>> print(bytearray_decode_unbound_method(s, 1))
    baab
    >>> print(bytearray_decode_unbound_method(s, None, 3))
    aba
    >>> print(bytearray_decode_unbound_method(s, 1, 4))
    baa

    >>> print(bytearray_decode_unbound_method(None))
    Traceback (most recent call last):
    TypeError: descriptor 'decode' requires a 'bytearray' object but received a 'NoneType'
    >>> print(bytearray_decode_unbound_method(None, 1))
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    >>> print(bytearray_decode_unbound_method(None, None, 1))
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    >>> print(bytearray_decode_unbound_method(None, 0, 1))
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    """
    if start is None:
        if stop is None:
            return bytearray.decode(s, 'utf8')
        else:
            return bytearray.decode(s[:stop], 'utf8')
    elif stop is None:
        return bytearray.decode(s[start:], 'utf8')
    else:
        return bytearray.decode(s[start:stop], 'utf8')

@cython.test_fail_if_path_exists('//SimpleCallNode')
@cython.test_assert_path_exists('//PythonCapiCallNode')
def bytearray_append(bytearray b, signed char c, int i, object o):
    """
    >>> b = bytearray(b'abc')
    >>> b = bytearray_append(b, ord('x'), ord('y'), ord('z'))
    >>> print(b.decode('ascii'))
    abcX@xyz

    >>> b = bytearray(b'abc')
    >>> b = bytearray_append(b, ord('x'), ord('y'), 0)
    >>> print(b.decode('ascii')[:-1])
    abcX@xy
    >>> b[-1]
    0

    >>> b = bytearray(b'abc')
    >>> b = bytearray_append(b, ord('x'), ord('y'), ord('z'))
    >>> print(b.decode('ascii'))
    abcX@xyz

    >>> b = bytearray(b'abc')
    >>> b = bytearray_append(b, ord('x'), ord('y'), ord('\\xc3'))
    >>> print(b[:-1].decode('ascii'))
    abcX@xy
    >>> print('%x' % b[-1])
    c3

    >>> b = bytearray(b'abc')
    >>> b = bytearray_append(b, ord('x'), 0xc3, 0xc3)
    >>> print(b.decode('iso8859-1'))
    abcX@xÃÃ

    >>> b = bytearray(b'abc')
    >>> b = bytearray_append(b, ord('x'), ord('y'), b'zz')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> print(b.decode('ascii'))
    abcX@xy

    >>> b = bytearray(b'abc')
    >>> b = bytearray_append(b, -1, ord('y'), ord('z'))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...
    >>> print(b.decode('ascii'))
    abcX@

    >>> b = bytearray(b'abc')
    >>> b = bytearray_append(b, ord('x'), -1, ord('z'))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...
    >>> print(b.decode('ascii'))
    abcX@x

    >>> b = bytearray(b'abc')
    >>> b = bytearray_append(b, ord('x'), 256, ord('z'))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...
    >>> print(b.decode('ascii'))
    abcX@x

    >>> b = bytearray(b'abc')
    >>> b = bytearray_append(b, ord('x'), ord('y'), -1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...
    >>> print(b.decode('ascii'))
    abcX@xy

    >>> b = bytearray(b'abc')
    >>> b = bytearray_append(b, ord('x'), ord('y'), 256)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...
    >>> print(b.decode('ascii'))
    abcX@xy

    >>> b = bytearray(b'abc')
    >>> b = bytearray_append(b, ord('x'), ord('y'), None)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> print(b.decode('ascii'))
    abcX@xy

    >>> b = bytearray_append(None, ord('x'), ord('y'), b'x')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'append'
    """
    assert b.append('X') is None
    b.append(64)
    b.append(c)
    b.append(i)
    b.append(o)
    return b


cdef class BytearraySubtype(bytearray):
    """
    >>> b = BytearraySubtype(b'abc')
    >>> b._append(ord('x'))
    >>> b.append(ord('y'))
    >>> print(b.decode('ascii'))
    abcxy
    """
    def _append(self, x):
        self.append(x)

def fromhex(bytearray b):
    """
    https://github.com/cython/cython/issues/5051
    Optimization of bound method calls was breaking classmethods
    >>> fromhex(bytearray(b""))
    """
    assert b.fromhex('2Ef0 F1f2  ') == b'.\xf0\xf1\xf2'


def bytearray_extend(bytearray b, value):
    """
    >>> bytearray_extend(bytearray(b''), b'xyz')
    b'xyz'
    >>> bytearray_extend(bytearray(b'abc'), b'xyz')
    b'abcxyz'
    >>> bytearray_extend(bytearray(b''), b'')
    b''
    >>> bytearray_extend(bytearray(b'abc'), b'')
    b'abc'

    >>> b = bytearray(b'')
    >>> bytearray_extend(b, b)
    b''
    >>> b = bytearray(b'xyz')
    >>> bytearray_extend(b, b)
    b'xyzxyz'

    >>> bytearray_extend(bytearray(b'abc'), None)
    Traceback (most recent call last):
    TypeError: can't extend bytearray with NoneType
   """
    b.extend(value)
    return bytes(b)


@cython.test_fail_if_path_exists('//SimpleCallNode[@function.attribute = "extend"]')
@cython.test_assert_path_exists('//PythonCapiCallNode')
def bytearray_extend_bytes(bytearray b, bytes arg):
    """
    >>> bytearray_extend_bytes(bytearray(b''), b'')
    b'aabcdefg'
    >>> bytearray_extend_bytes(bytearray(b'xx'), b'yy')
    b'xxaabcdefgyy'
    >>> bytearray_extend_bytes(bytearray(b'xx'), None)
    Traceback (most recent call last):
    TypeError: can't extend bytearray with NoneType
    """
    b.extend(b'')
    b.extend(b'a')
    b.extend(b'')
    b.extend(b'abcdefg')
    b.extend(b'')
    b.extend(arg)
    return bytes(b)


def bytearray_extend_bytearray(bytearray b):
    """
    >>> b = bytearray(b'')
    >>> bytearray_extend_bytearray(b)
    b'aabcdefg'
    """
    b.extend(bytearray(b''))
    b.extend(bytearray(b'a'))
    b.extend(bytearray(b''))
    b.extend(bytearray(b'abcdefg'))
    b.extend(bytearray(b''))
    return bytes(b)
