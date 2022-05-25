# mode: run
# tag: forin, builtins, reversed, enumerate

cimport cython

import sys
IS_PY3 = sys.version_info[0] >= 3
IS_32BIT_PY2 = not IS_PY3 and sys.maxint < 2**32


def unlongify(v):
    # on 32bit Py2.x platforms, 'unsigned int' coerces to a Python long => fix doctest output here.
    s = repr(v)
    if IS_32BIT_PY2:
        assert s.count('L') == s.count(',') + 1, s
        s = s.replace('L', '')
    return s


def _reversed(it):
    return list(it)[::-1]

@cython.test_assert_path_exists('//ForInStatNode',
                                '//ForInStatNode/IteratorNode',
                                '//ForInStatNode/IteratorNode[@reversed = True]',
                                )
@cython.test_fail_if_path_exists('//ForInStatNode/IteratorNode//SimpleCallNode')
def reversed_list(list l):
    """
    >>> [ i for i in _reversed([1,2,3,4]) ]
    [4, 3, 2, 1]
    >>> reversed_list([1,2,3,4])
    [4, 3, 2, 1]
    >>> reversed_list([])
    []
    >>> reversed_list(None)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not iterable
    """
    result = []
    for item in reversed(l):
        result.append(item)
    return result

@cython.test_assert_path_exists('//ForInStatNode',
                                '//ForInStatNode/IteratorNode',
                                '//ForInStatNode/IteratorNode[@reversed = True]',
                                )
@cython.test_fail_if_path_exists('//ForInStatNode/IteratorNode//SimpleCallNode')
def reversed_tuple(tuple t):
    """
    >>> [ i for i in _reversed((1,2,3,4)) ]
    [4, 3, 2, 1]
    >>> reversed_tuple((1,2,3,4))
    [4, 3, 2, 1]
    >>> reversed_tuple(())
    []
    >>> reversed_tuple(None)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not iterable
    """
    result = []
    for item in reversed(t):
        result.append(item)
    return result

@cython.test_assert_path_exists('//ForInStatNode',
                                '//ForInStatNode/IteratorNode',
                                '//ForInStatNode/IteratorNode[@reversed = True]',
                                )
@cython.test_fail_if_path_exists('//ForInStatNode/IteratorNode//SimpleCallNode')
def enumerate_reversed_list(list l):
    """
    >>> list(enumerate(_reversed([1,2,3])))
    [(0, 3), (1, 2), (2, 1)]
    >>> enumerate_reversed_list([1,2,3])
    [(0, 3), (1, 2), (2, 1)]
    >>> enumerate_reversed_list([])
    []
    >>> enumerate_reversed_list(None)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not iterable
    """
    result = []
    cdef Py_ssize_t i
    for i, item in enumerate(reversed(l)):
        result.append((i, item))
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_range(int N):
    """
    >>> [ i for i in _reversed(range(5)) ]
    [4, 3, 2, 1, 0]
    >>> reversed_range(5)
    ([4, 3, 2, 1, 0], 0)

    >>> [ i for i in _reversed(range(0)) ]
    []
    >>> reversed_range(0)
    ([], 99)
    """
    cdef int i = 99
    result = []
    for i in reversed(range(N)):
        result.append(i)
    return result, i

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_range_step_pos(int a, int b):
    """
    >>> [ i for i in _reversed(range(0, 5, 1)) ]
    [4, 3, 2, 1, 0]
    >>> reversed_range_step_pos(0, 5)
    ([4, 3, 2, 1, 0], 0)

    >>> [ i for i in _reversed(range(5, 0, 1)) ]
    []
    >>> reversed_range_step_pos(5, 0)
    ([], 99)
    """
    cdef int i = 99
    result = []
    for i in reversed(range(a, b, 1)):
        result.append(i)
    return result, i

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_range_step_neg(int a, int b):
    """
    >>> [ i for i in _reversed(range(5, -1, -1)) ]
    [0, 1, 2, 3, 4, 5]
    >>> reversed_range_step_neg(5, -1)
    ([0, 1, 2, 3, 4, 5], 5)

    >>> [ i for i in _reversed(range(0, 5, -1)) ]
    []
    >>> reversed_range_step_neg(0, 5)
    ([], 99)
    """
    cdef int i = 99
    result = []
    for i in reversed(range(a, b, -1)):
        result.append(i)
    return result, i

@cython.test_assert_path_exists('//ForFromStatNode')
@cython.test_fail_if_path_exists('//ForInStatNode')
def reversed_range_step3(int a, int b):
    """
    >>> [ i for i in _reversed(range(-5, 0, 3)) ]
    [-2, -5]
    >>> reversed_range_step3(-5, 0)
    ([-2, -5], -5)

    >>> [ i for i in _reversed(range(0, 5, 3)) ]
    [3, 0]
    >>> reversed_range_step3(0, 5)
    ([3, 0], 0)

    >>> [ i for i in _reversed(range(5, 0, 3)) ]
    []
    >>> reversed_range_step3(5, 0)
    ([], 99)

    >>> [ i for i in _reversed(range(1, 1, 3)) ]
    []
    >>> reversed_range_step3(1, 1)
    ([], 99)
    """
    cdef int i = 99
    result = []
    for i in reversed(range(a, b, 3)):
        result.append(i)
    return result, i

@cython.test_assert_path_exists('//ForFromStatNode')
@cython.test_fail_if_path_exists('//ForInStatNode')
def reversed_range_step3_expr(int a, int b):
    """
    >>> [ i for i in _reversed(range(0, 5, 3)) ]
    [3, 0]
    >>> reversed_range_step3_expr(0, 5)
    ([3, 0], 0)
    """
    cdef int i = 99, c = 100
    result = []
    for i in reversed(range(c-c + a + c-c, c-c + b + c-c, 3)):
        result.append(i)
    return result, i

@cython.test_assert_path_exists('//ForFromStatNode')
@cython.test_fail_if_path_exists('//ForInStatNode')
def reversed_range_step3_neg(int a, int b):
    """
    >>> [ i for i in _reversed(range(0, -5, -3)) ]
    [-3, 0]
    >>> reversed_range_step3_neg(0, -5)
    ([-3, 0], 0)

    >>> [ i for i in _reversed(range(5, 0, -3)) ]
    [2, 5]
    >>> reversed_range_step3_neg(5, 0)
    ([2, 5], 5)

    >>> [ i for i in _reversed(range(0, 5, -3)) ]
    []
    >>> reversed_range_step3_neg(0, 5)
    ([], 99)

    >>> [ i for i in _reversed(range(1, 1, -3)) ]
    []
    >>> reversed_range_step3_neg(1, 1)
    ([], 99)
    """
    cdef int i = 99
    result = []
    for i in reversed(range(a, b, -3)):
        result.append(i)
    return result, i

@cython.test_assert_path_exists('//ForFromStatNode')
@cython.test_fail_if_path_exists('//ForInStatNode')
def reversed_range_step3_neg_expr(int a, int b):
    """
    >>> [ i for i in _reversed(range(5, 0, -3)) ]
    [2, 5]
    >>> reversed_range_step3_neg_expr(5, 0)
    ([2, 5], 5)
    """
    cdef int i = 99, c = 100
    result = []
    for i in reversed(range(c-c + a + c-c, c-c + b + c-c, -3)):
        result.append(i)
    return result, i

def reversed_range_step3_py_args(a, b):
    """
    >>> [ i for i in _reversed(range(-5, 0, 3)) ]
    [-2, -5]
    >>> reversed_range_step3_py_args(-5, 0)
    ([-2, -5], -5)

    >>> [ i for i in _reversed(range(0, 5, 3)) ]
    [3, 0]
    >>> reversed_range_step3_py_args(0, 5)
    ([3, 0], 0)

    >>> [ i for i in _reversed(range(5, 0, 3)) ]
    []
    >>> reversed_range_step3_py_args(5, 0)
    ([], 99)

    >>> [ i for i in _reversed(range(1, 1, 3)) ]
    []
    >>> reversed_range_step3_py_args(1, 1)
    ([], 99)

    >>> reversed_range_step3_py_args(set(), 1) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...integer...

    >>> reversed_range_step3_py_args(1, set()) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...integer...
    """
    i = 99
    result = []
    for i in reversed(range(a, b, 3)):
        result.append(i)
    return result, i

def reversed_range_step3_neg_py_args(a, b):
    """
    >>> [ i for i in _reversed(range(0, -5, -3)) ]
    [-3, 0]
    >>> reversed_range_step3_neg_py_args(0, -5)
    ([-3, 0], 0)

    >>> [ i for i in _reversed(range(5, 0, -3)) ]
    [2, 5]
    >>> reversed_range_step3_neg_py_args(5, 0)
    ([2, 5], 5)

    >>> [ i for i in _reversed(range(0, 5, -3)) ]
    []
    >>> reversed_range_step3_neg_py_args(0, 5)
    ([], 99)

    >>> [ i for i in _reversed(range(1, 1, -3)) ]
    []
    >>> reversed_range_step3_neg_py_args(1, 1)
    ([], 99)

    >>> reversed_range_step3_neg_py_args(set(), 1) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...integer...

    >>> reversed_range_step3_neg_py_args(1, set()) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...integer...
    """
    i = 99
    result = []
    for i in reversed(range(a, b, -3)):
        result.append(i)
    return result, i

def reversed_range_step3_py_obj_left(a, int b):
    """
    >>> reversed_range_step3_py_obj_left(set(), 0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...int...
    """
    cdef long i
    result = []
    for i in reversed(range(a, b, 3)):
        result.append(i)

def reversed_range_step3_py_obj_right(int a, b):
    """
    >>> reversed_range_step3_py_obj_right(0, set())  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...int...
    """
    cdef long i
    result = []
    for i in reversed(range(a, b, 3)):
        result.append(i)

def reversed_range_step3_neg_py_obj_left(a, int b):
    """
    >>> reversed_range_step3_neg_py_obj_left(set(), 0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...int...
    """
    cdef long i
    result = []
    for i in reversed(range(a, b, -3)):
        result.append(i)

def reversed_range_step3_neg_py_obj_right(int a, b):
    """
    >>> reversed_range_step3_py_obj_right(0, set())  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...int...
    """
    cdef long i
    result = []
    for i in reversed(range(a, b, -3)):
        result.append(i)

@cython.test_fail_if_path_exists('//ForInStatNode')
def reversed_range_constant():
    """
    >>> [ i for i in _reversed(range(-12, -2, 4)) ]
    [-4, -8, -12]
    >>> reversed_range_constant()
    ([-4, -8, -12], -12)
    """
    cdef int i = 99
    result = []
    for i in reversed(range(1, 1, 4)):
        result.append(i)
    assert result == list(reversed(range(1, 1, 4))), result
    assert i == 99

    for i in reversed(range(1, 1, 1)):
        result.append(i)
    assert result == list(reversed(range(1, 1, 1))), result

    result = []
    for i in reversed(range(0, 1, 4)):
        result.append(i)
    assert result == list(reversed(range(0, 1, 4))), result

    result = []
    for i in reversed(range(0, 1, 1)):
        result.append(i)
    assert result == list(reversed(range(0, 1, 1))), result

    result = []
    for i in reversed(range(1, 8, 4)):
        result.append(i)
    assert result == list(reversed(range(1, 8, 4))), result

    result = []
    for i in reversed(range(1, 8, 1)):
        result.append(i)
    assert result == list(reversed(range(1, 8, 1))), result

    result = []
    for i in reversed(range(1, 9, 4)):
        result.append(i)
    assert result == list(reversed(range(1, 9, 4))), result

    result = []
    for i in reversed(range(1, 10, 4)):
        result.append(i)
    assert result == list(reversed(range(1, 10, 4))), result

    result = []
    for i in reversed(range(1, 11, 4)):
        result.append(i)
    assert result == list(reversed(range(1, 11, 4))), result

    result = []
    for i in reversed(range(1, 12, 4)):
        result.append(i)
    assert result == list(reversed(range(1, 12, 4))), result

    result = []
    for i in reversed(range(0, 8, 4)):
        result.append(i)
    assert result == list(reversed(range(0, 8, 4))), result

    result = []
    for i in reversed(range(0, 9, 4)):
        result.append(i)
    assert result == list(reversed(range(0, 9, 4))), result

    result = []
    for i in reversed(range(0, 10, 4)):
        result.append(i)
    assert result == list(reversed(range(0, 10, 4))), result

    result = []
    for i in reversed(range(0, 11, 4)):
        result.append(i)
    assert result == list(reversed(range(0, 11, 4))), result

    result = []
    for i in reversed(range(0, 12, 4)):
        result.append(i)
    assert result == list(reversed(range(0, 12, 4))), result

    i = 99
    result = []
    for i in reversed(range(-12, -2, 4)):
        result.append(i)
    assert result == list(reversed(range(-12, -2, 4))), result
    return result, i

@cython.test_assert_path_exists('//ForFromStatNode')
@cython.test_fail_if_path_exists('//ForInStatNode')
def reversed_range_constant_neg():
    """
    >>> [ i for i in _reversed(range(-2, -12, -4)) ]
    [-10, -6, -2]
    >>> reversed_range_constant_neg()
    """
    cdef int i = 99
    result = []
    for i in reversed(range(1, 1, -4)):
        result.append(i)
    assert result == list(reversed(range(1, 1, -4))), result
    assert i == 99

    result = []
    for i in reversed(range(1, 1, -1)):
        result.append(i)
    assert result == list(reversed(range(1, 1, -1))), result

    result = []
    for i in reversed(range(1, 0, -4)):
        result.append(i)
    assert result == list(reversed(range(1, 0, -4))), result

    result = []
    for i in reversed(range(1, 0, -1)):
        result.append(i)
    assert result == list(reversed(range(1, 0, -1))), result

    result = []
    for i in reversed(range(8, 1, -4)):
        result.append(i)
    assert result == list(reversed(range(8, 1, -4))), result

    result = []
    for i in reversed(range(8, 1, -1)):
        result.append(i)
    assert result == list(reversed(range(8, 1, -1))), result

    result = []
    for i in reversed(range(9, 1, -4)):
        result.append(i)
    assert result == list(reversed(range(9, 1, -4))), result

    result = []
    for i in reversed(range(9, 1, -1)):
        result.append(i)
    assert result == list(reversed(range(9, 1, -1))), result

    result = []
    for i in reversed(range(10, 1, -4)):
        result.append(i)
    assert result == list(reversed(range(10, 1, -4))), result

    result = []
    for i in reversed(range(11, 1, -4)):
        result.append(i)
    assert result == list(reversed(range(11, 1, -4))), result

    result = []
    for i in reversed(range(11, 1, -1)):
        result.append(i)
    assert result == list(reversed(range(11, 1, -1))), result

    result = []
    for i in reversed(range(12, 1, -4)):
        result.append(i)
    assert result == list(reversed(range(12, 1, -4))), result

    result = []
    for i in reversed(range(12, 1, -1)):
        result.append(i)
    assert result == list(reversed(range(12, 1, -1))), result

    result = []
    for i in reversed(range(8, 0, -4)):
        result.append(i)
    assert result == list(reversed(range(8, 0, -4))), result

    result = []
    for i in reversed(range(8, 0, -1)):
        result.append(i)
    assert result == list(reversed(range(8, 0, -1))), result

    result = []
    for i in reversed(range(9, 0, -4)):
        result.append(i)
    assert result == list(reversed(range(9, 0, -4))), result

    result = []
    for i in reversed(range(9, 0, -1)):
        result.append(i)
    assert result == list(reversed(range(9, 0, -1))), result

    result = []
    for i in reversed(range(10, 0, -4)):
        result.append(i)
    assert result == list(reversed(range(10, 0, -4))), result

    result = []
    for i in reversed(range(10, 0, -1)):
        result.append(i)
    assert result == list(reversed(range(10, 0, -1))), result

    result = []
    for i in reversed(range(11, 0, -4)):
        result.append(i)
    assert result == list(reversed(range(11, 0, -4))), result

    result = []
    for i in reversed(range(11, 0, -1)):
        result.append(i)
    assert result == list(reversed(range(11, 0, -1))), result

    result = []
    for i in reversed(range(12, 0, -4)):
        result.append(i)
    assert result == list(reversed(range(12, 0, -4))), result

    result = []
    for i in reversed(range(12, 0, -1)):
        result.append(i)
    assert result == list(reversed(range(12, 0, -1))), result

    result = []
    for i in reversed(range(-2, -12, -4)):
        result.append(i)
    assert result == list(reversed(range(-2, -12, -4))), result

    result = []
    for i in reversed(range(-2, -12, -1)):
        result.append(i)
    assert result == list(reversed(range(-2, -12, -1))), result

unicode_string = u"abcDEF"

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_unicode(unicode u):
    """
    >>> print(''.join(_reversed(unicode_string)))
    FEDcba
    >>> print(''.join(reversed_unicode(unicode_string)))
    FEDcba
    """
    result = []
    for c in reversed(u):
        result.append(c)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_unicode_slice(unicode u):
    """
    >>> print(''.join(_reversed(unicode_string[1:-2])))
    Dcb
    >>> print(''.join(reversed_unicode_slice(unicode_string)))
    Dcb
    """
    result = []
    for c in reversed(u[1:-2]):
        result.append(c)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_unicode_slice_neg_step(unicode u):
    """
    >>> print(''.join(_reversed(unicode_string[-2:1:-1])))
    cDE
    >>> print(''.join(reversed_unicode_slice_neg_step(unicode_string)))
    cDE
    """
    result = []
    for c in reversed(u[-2:1:-1]):
        result.append(c)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_unicode_slice_pos_step(unicode u):
    """
    >>> print(''.join(_reversed(unicode_string[1:-2:1])))
    Dcb
    >>> print(''.join(reversed_unicode_slice_pos_step(unicode_string)))
    Dcb
    """
    result = []
    for c in reversed(u[1:-2:1]):
        result.append(c)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_unicode_slice_start_pos_step(unicode u):
    """
    >>> print(''.join(_reversed(unicode_string[2::1])))
    FEDc
    >>> print(''.join(reversed_unicode_slice_start_pos_step(unicode_string)))
    FEDc
    """
    result = []
    for c in reversed(u[2::1]):
        result.append(c)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_unicode_slice_start_neg_step(unicode u):
    """
    >>> print(''.join(_reversed(unicode_string[3::-1])))
    abcD
    >>> print(''.join(reversed_unicode_slice_start_neg_step(unicode_string)))
    abcD
    """
    result = []
    for c in reversed(u[3::-1]):
        result.append(c)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_unicode_slice_end_pos_step(unicode u):
    """
    >>> print(''.join(_reversed(unicode_string[:-2:1])))
    Dcba
    >>> print(''.join(reversed_unicode_slice_end_pos_step(unicode_string)))
    Dcba
    """
    result = []
    for c in reversed(u[:-2:1]):
        result.append(c)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_unicode_slice_end_neg_step(unicode u):
    """
    >>> print(''.join(_reversed(unicode_string[:-3:-1])))
    EF
    >>> print(''.join(reversed_unicode_slice_end_neg_step(unicode_string)))
    EF
    """
    result = []
    for c in reversed(u[:-3:-1]):
        result.append(c)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_unicode_slice_neg_step_only(unicode u):
    """
    >>> print(''.join(_reversed(unicode_string[::-1])))
    abcDEF
    >>> print(''.join(reversed_unicode_slice_neg_step_only(unicode_string)))
    abcDEF
    """
    result = []
    for c in reversed(u[::-1]):
        result.append(c)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_unicode_slice_pos_step_only(unicode u):
    """
    >>> print(''.join(_reversed(unicode_string[::1])))
    FEDcba
    >>> print(''.join(reversed_unicode_slice_pos_step_only(unicode_string)))
    FEDcba
    """
    result = []
    for c in reversed(u[::1]):
        result.append(c)
    return result

bytes_string = b'abcDEF'
join_bytes = b''.join

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_bytes(bytes s):
    """
    >>> b = IS_PY3 and bytes_string or map(ord, bytes_string)
    >>> list(_reversed(b))
    [70, 69, 68, 99, 98, 97]
    >>> reversed_bytes(bytes_string)
    [70, 69, 68, 99, 98, 97]
    """
    cdef char c
    result = []
    for c in reversed(s):
        result.append(c)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_bytes_slice(bytes s):
    """
    >>> b = IS_PY3 and bytes_string or map(ord, bytes_string)
    >>> list(_reversed(b[1:-2]))
    [68, 99, 98]
    >>> reversed_bytes_slice(bytes_string)
    [68, 99, 98]
    """
    cdef char c
    result = []
    for c in reversed(s[1:-2]):
        result.append(c)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_bytes_slice_step(bytes s):
    """
    >>> b = IS_PY3 and bytes_string or map(ord, bytes_string)
    >>> list(_reversed(b[-2:1:-1]))
    [99, 68, 69]
    >>> reversed_bytes_slice_step(bytes_string)
    [99, 68, 69]
    """
    cdef char c
    result = []
    for c in reversed(s[-2:1:-1]):
        result.append(c)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_bytes_slice_step_only(bytes s):
    """
    >>> b = IS_PY3 and bytes_string or map(ord, bytes_string)
    >>> list(_reversed(b[::-1]))
    [97, 98, 99, 68, 69, 70]
    >>> reversed_bytes_slice_step_only(bytes_string)
    [97, 98, 99, 68, 69, 70]
    """
    cdef char c
    result = []
    for c in reversed(s[::-1]):
        result.append(c)
    return result


@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_unsigned(int a, int b):
    """
    >>> unlongify(reversed_unsigned(0, 5))
    '[4, 3, 2, 1, 0]'
    >>> unlongify(reversed_unsigned(1, 5))
    '[4, 3, 2, 1]'
    >>> reversed_unsigned(1, 1)
    []
    """
    cdef unsigned int i
    return [i for i in reversed(range(a, b))]

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_unsigned_by_3(int a, int b):
    """
    >>> unlongify(reversed_unsigned_by_3(0, 5))
    '[3, 0]'
    >>> unlongify(reversed_unsigned_by_3(0, 7))
    '[6, 3, 0]'
    """
    cdef unsigned int i
    return [i for i in reversed(range(a, b, 3))]

@cython.test_assert_path_exists('//ForFromStatNode')
def range_unsigned_by_neg_3(int a, int b):
    """
    >>> unlongify(range_unsigned_by_neg_3(-1, 6))
    '[6, 3, 0]'
    >>> unlongify(range_unsigned_by_neg_3(0, 7))
    '[7, 4, 1]'
    """
    cdef unsigned int i
    return [i for i in range(b, a, -3)]
