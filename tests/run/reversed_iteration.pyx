# mode: run
# tag: forin, builtins, reversed, enumerate

cimport cython

import sys
IS_PY3 = sys.version_info[0] >= 3

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

#@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_range_step3(int a, int b):
    """
    >>> [ i for i in _reversed(range(0, 5, 3)) ]
    [3, 0]
    >>> reversed_range_step3(0, 5)
    ([3, 0], 0)

    >>> [ i for i in _reversed(range(5, 0, 3)) ]
    []
    >>> reversed_range_step3(5, 0)
    ([], 99)
    """
    cdef int i = 99
    result = []
    for i in reversed(range(a, b, 3)):
        result.append(i)
    return result, i

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
def reversed_unicode_slice_step(unicode u):
    """
    >>> print(''.join(_reversed(unicode_string[-2:1:-1])))
    cDE
    >>> print(''.join(reversed_unicode_slice_step(unicode_string)))
    cDE
    """
    result = []
    for c in reversed(u[-2:1:-1]):
        result.append(c)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_unicode_slice_step_only(unicode u):
    """
    >>> print(''.join(_reversed(unicode_string[::-1])))
    abcDEF
    >>> print(''.join(reversed_unicode_slice_step_only(unicode_string)))
    abcDEF
    """
    result = []
    for c in reversed(u[::-1]):
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
