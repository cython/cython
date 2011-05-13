
cimport cython

def _reversed(it):
    return list(it)[::-1]

def reversed_list(list l):
    """
    >>> [ i for i in _reversed([1,2,3,4]) ]
    [4, 3, 2, 1]
    >>> reversed_list([1,2,3,4])
    [4, 3, 2, 1]
    """
    result = []
    for item in reversed(l):
        result.append(item)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_range(int N):
    """
    >>> i = 99
    >>> [ i for i in _reversed(range(5)) ], i
    ([4, 3, 2, 1, 0], 0)
    >>> reversed_range(5)
    ([4, 3, 2, 1, 0], 0)

    >>> i = 99
    >>> ([ i for i in _reversed(range(0)) ], i)
    ([], 99)
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
    >>> print(join_bytes(_reversed(bytes_string)).decode('ASCII'))
    FEDcba
    >>> print(join_bytes(reversed_bytes(bytes_string)).decode('ASCII'))
    FEDcba
    """
    result = []
    for c in reversed(s):
        result.append(c)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_bytes_slice(bytes s):
    """
    >>> print(join_bytes(_reversed(bytes_string[1:-2])).decode('ASCII'))
    Dcb
    >>> print(join_bytes(reversed_bytes_slice(bytes_string)).decode('ASCII'))
    Dcb
    """
    result = []
    for c in reversed(s[1:-2]):
        result.append(c)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_bytes_slice_step(bytes s):
    """
    >>> print(join_bytes(_reversed(bytes_string[-2:1:-1])).decode('ASCII'))
    cDE
    >>> print(join_bytes(reversed_bytes_slice_step(bytes_string)).decode('ASCII'))
    cDE
    """
    result = []
    for c in reversed(s[-2:1:-1]):
        result.append(c)
    return result

@cython.test_assert_path_exists('//ForFromStatNode')
def reversed_bytes_slice_step_only(bytes s):
    """
    >>> print(join_bytes(_reversed(bytes_string[::-1])).decode('ASCII'))
    abcDEF
    >>> print(join_bytes(reversed_bytes_slice_step_only(bytes_string)).decode('ASCII'))
    abcDEF
    """
    result = []
    for c in reversed(s[::-1]):
        result.append(c)
    return result
