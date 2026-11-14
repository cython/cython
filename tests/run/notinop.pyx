
cimport cython

def f(a,b):
    """
    >>> f(1,[1,2,3])
    False
    >>> f(5,[1,2,3])
    True
    >>> f(2,(1,2,3))
    False
    """
    result = a not in b
    return result

def g(a,b):
    """
    >>> g(1,[1,2,3])
    0
    >>> g(5,[1,2,3])
    1
    >>> g(2,(1,2,3))
    0
    """
    cdef int result
    result = a not in b
    return result

def h(b):
    """
    >>> h([1,2,3,4])
    False
    >>> h([1,3,4])
    True
    """
    result = 2 not in b
    return result

def j(b):
    """
    >>> j([1,2,3,4])
    0
    >>> j([1,3,4])
    1
    """
    cdef int result
    result = 2 not in b
    return result

@cython.test_fail_if_path_exists("//SwitchStatNode")
def k(a):
    """
    >>> k(1)
    0
    >>> k(5)
    1
    """
    cdef int result = a not in [1,2,3,4]
    return result

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//PrimaryCmpNode")
def m_list(int a):
    """
    >>> m_list(2)
    0
    >>> m_list(5)
    1
    """
    cdef int result = a not in [1,2,3,4]
    return result

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//PrimaryCmpNode")
def m_tuple(int a):
    """
    >>> m_tuple(2)
    0
    >>> m_tuple(5)
    1
    """
    cdef int result = a not in (1,2,3,4)
    return result

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//BoolBinopNode", "//PrimaryCmpNode")
def m_set(int a):
    """
    >>> m_set(2)
    0
    >>> m_set(5)
    1
    """
    cdef int result = a not in {1,2,3,4}
    return result

cdef bytes bytes_string = b'abcdefg'
py_bytes_string = bytes_string

@cython.test_assert_path_exists("//PrimaryCmpNode")
@cython.test_fail_if_path_exists("//SwitchStatNode", "//BoolBinopNode", "//BoolBinopNode")
def m_bytes(char a):
    """
    >>> m_bytes(ord('f'))
    0
    >>> m_bytes(ord('X'))
    1
    """
    cdef int result = a not in bytes_string
    return result

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//BoolBinopNode", "//PrimaryCmpNode")
def m_bytes_literal(char a):
    """
    >>> m_bytes_literal(ord('f'))
    0
    >>> m_bytes_literal(ord('X'))
    1
    """
    cdef int result = a not in b'abcdefg'
    return result


@cython.test_assert_path_exists("//PrimaryCmpNode")
@cython.test_fail_if_path_exists("//SwitchStatNode", "//BoolBinopNode")
def m_bytearray(char a, bytearray bytearray_string):
    """
    >>> m_bytearray(ord('f'), bytearray(py_bytes_string))
    0
    >>> m_bytearray(ord('X'), bytearray(py_bytes_string))
    1
    >>> 'f'.encode('ASCII') in None    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...iterable...
    >>> m_bytearray(ord('f'), None)
    Traceback (most recent call last):
    TypeError: argument of type 'NoneType' is not iterable
    """
    cdef int result = a not in bytearray_string
    return result


@cython.test_assert_path_exists("//PrimaryCmpNode")
@cython.test_fail_if_path_exists("//SwitchStatNode", "//BoolBinopNode")
def m_literal_in_bytes(bytes bytes_string):
    """
    >>> m_literal_in_bytes(py_bytes_string)
    0
    >>> m_literal_in_bytes(py_bytes_string.replace(b'f', b'F'))
    1
    >>> 'f'.encode('ASCII') in None    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...iterable...
    >>> m_literal_in_bytes(None)
    Traceback (most recent call last):
    TypeError: argument of type 'NoneType' is not iterable
    """
    cdef int result = b'f' not in bytes_string
    return result


@cython.test_assert_path_exists("//PrimaryCmpNode")
@cython.test_fail_if_path_exists("//SwitchStatNode", "//BoolBinopNode")
def m_literal_in_bytearray(bytearray bytearray_string):
    """
    >>> m_literal_in_bytearray(bytearray(py_bytes_string))
    0
    >>> m_literal_in_bytearray(bytearray(py_bytes_string.replace(b'f', b'F')))
    1
    >>> 'f'.encode('ASCII') in None    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...iterable...
    >>> m_literal_in_bytearray(None)
    Traceback (most recent call last):
    TypeError: argument of type 'NoneType' is not iterable
    """
    cdef int result = b'f' not in bytearray_string
    return result


cdef unicode unicode_string = u'abcdefg\u1234\uF8D2'
py_unicode_string = unicode_string

cdef unicode klingon_character = u'\uF8D2'
py_klingon_character = klingon_character

cdef unicode wide_unicode_character = u'\U0010FEDC'
py_wide_unicode_character = wide_unicode_character


@cython.test_assert_path_exists("//PrimaryCmpNode")
@cython.test_fail_if_path_exists("//SwitchStatNode", "//BoolBinopNode", "//BoolBinopNode")
def m_unicode(Py_UCS4 a, unicode unicode_string):
    """
    >>> m_unicode(ord('f'), py_unicode_string)
    0
    >>> m_unicode(ord('X'), py_unicode_string)
    1
    >>> m_unicode(ord(py_klingon_character), py_unicode_string)
    0

    >>> 'f' in None    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...iterable...
    >>> m_unicode(ord('f'), None)
    Traceback (most recent call last):
    TypeError: argument of type 'NoneType' is not iterable
    """
    cdef int result = a not in unicode_string
    return result


@cython.test_assert_path_exists("//PrimaryCmpNode")
@cython.test_fail_if_path_exists("//SwitchStatNode", "//BoolBinopNode")
def m_literal_in_unicode(unicode unicode_string):
    """
    >>> m_literal_in_unicode(py_unicode_string)
    0
    >>> m_literal_in_unicode(py_unicode_string.replace('f', 'F'))
    1

    >>> 'f' in None   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...iterable...
    >>> m_literal_in_unicode(None)
    Traceback (most recent call last):
    TypeError: argument of type 'NoneType' is not iterable
    """
    cdef int result = 'f' not in unicode_string
    return result


@cython.test_assert_path_exists("//PrimaryCmpNode")
@cython.test_fail_if_path_exists("//SwitchStatNode", "//BoolBinopNode")
def m_literal_in_unicode_cascade(unicode unicode_string):
    """
    >>> m_literal_in_unicode_cascade(py_unicode_string)
    0
    >>> m_literal_in_unicode_cascade(py_unicode_string.replace('f', 'F'))
    1

    >>> 'f' in None   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...iterable...
    >>> m_literal_in_unicode_cascade(None)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...iterable...
    """
    cdef int result = 'f' not in unicode_string in unicode_string
    return result


@cython.test_fail_if_path_exists("//SwitchStatNode", "//BoolBinopNode", "//BoolBinopNode")
def m_str_notin_str(str a, str unicode_string):
    """
    >>> m_str_notin_str('f', py_unicode_string)
    0
    >>> m_str_notin_str('ef', py_unicode_string)
    0
    >>> m_str_notin_str('ff', py_unicode_string)
    1
    >>> m_str_notin_str('X', py_unicode_string)
    1
    >>> m_str_notin_str('XX', py_unicode_string)
    1
    >>> m_str_notin_str(py_klingon_character, py_unicode_string)
    0

    >>> 'f' in None    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...iterable...
    >>> m_str_notin_str('f', None)
    Traceback (most recent call last):
    TypeError: argument of type 'NoneType' is not iterable
    >>> m_str_notin_str(None, 'f')    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...NoneType...
    >>> m_str_notin_str(None, None)
    Traceback (most recent call last):
    TypeError: argument of type 'NoneType' is not iterable
    """
    cdef int result = a not in unicode_string
    return result


@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//BoolBinopNode", "//PrimaryCmpNode")
def m_unicode_literal(Py_UCS4 a):
    """
    >>> m_unicode_literal(ord('f'))
    0
    >>> m_unicode_literal(ord('X'))
    1
    >>> m_unicode_literal(ord(py_klingon_character))
    0
    """
    cdef int result = a not in u'abcdefg\u1234\uF8D2'
    return result


@cython.test_assert_path_exists("//PrimaryCmpNode", "//CascadedCmpNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//SwitchStatNode")
def m_unicode_char_cascade_notin_char(Py_UCS4 a, str cascade):
    """
    >>> m_unicode_char_cascade_notin_char(ord('f'), 'f')
    0
    >>> m_unicode_char_cascade_notin_char(ord('X'), 'abc\\0defg\\u1234\\uF8D2\\U0010FEDC')
    0
    >>> m_unicode_char_cascade_notin_char(ord('f'), 'abc\\0de XXX g\\u1234\\uF8D2\\U0010FEDC')
    0
    >>> m_unicode_char_cascade_notin_char(ord('X'), 'abc\\0de XXX g\\u1234\\uF8D2\\U0010FEDC')
    1
    >>> m_unicode_char_cascade_notin_char(ord(py_wide_unicode_character), 'abc\\0defg\\u1234\\uF8D2\\U0010FEDC')
    0
    >>> m_unicode_char_cascade_notin_char(ord(py_wide_unicode_character), 'abc\\0de XXX g\\u1234\\uF8D2\\U0010FEDC')
    1
    """
    cdef int result = a not in 'f' not in cascade
    return result


@cython.test_assert_path_exists("//PrimaryCmpNode", "//CascadedCmpNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//SwitchStatNode")
def m_unicode_char_cascade_notin(str a, str cascade):
    """
    >>> m_unicode_char_cascade_notin('f', 'abc\\0defg\\u1234\\uF8D2\\U0010FEDC')
    0
    >>> m_unicode_char_cascade_notin('f', 'abc\\0de XXX g\\u1234\\uF8D2\\U0010FEDC')
    0
    >>> m_unicode_char_cascade_notin('X', 'abc\\0defg\\u1234\\uF8D2\\U0010FEDC')
    0
    >>> m_unicode_char_cascade_notin('fX', 'abc\\0de XXX g\\u1234\\uF8D2\\U0010FEDC')
    1
    >>> m_unicode_char_cascade_notin(py_wide_unicode_character, 'abc\\0defg\\u1234\\uF8D2\\U0010FEDC')
    0
    >>> m_unicode_char_cascade_notin(py_wide_unicode_character, 'abc\\0de XXX g\\u1234\\uF8D2\\U0010FEDC')
    1
    """
    cdef int result = a not in 'f' not in cascade
    return result


@cython.test_assert_path_exists("//PrimaryCmpNode", "//CascadedCmpNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//SwitchStatNode")
def m_wide_unicode_literal_cascade_notin(Py_UCS4 a, str cascade):
    """
    >>> m_wide_unicode_literal_cascade_notin(ord('f'), 'abc\\0defg\\u1234\\uF8D2\\U0010FEDC')
    0
    >>> m_wide_unicode_literal_cascade_notin(ord('X'), '  abc\\0defg\\u1234\\uF8D2\\U0010FEDC  ')
    0
    >>> m_wide_unicode_literal_cascade_notin(ord('X'), 'abc\\0defg\\u1234 XXX \\uF8D2\\U0010FEDC')
    1
    >>> m_wide_unicode_literal_cascade_notin(ord(py_wide_unicode_character), 'abc\\0defg\\u1234\\uF8D2\\U0010FEDC')
    0
    """
    cdef int result = a not in u'abc\0defg\u1234\uF8D2\U0010FEDC' not in cascade
    return result


@cython.test_assert_path_exists("//PrimaryCmpNode", "//CascadedCmpNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//SwitchStatNode")
def m_wide_unicode_literal_cascade_eq(Py_UCS4 a, str cascade):
    """
    >>> m_wide_unicode_literal_cascade_eq(ord('f'), 'abc\\0defg\\u1234\\uF8D2\\U0010FEDC')
    1
    >>> m_wide_unicode_literal_cascade_eq(ord('f'), 'abc\\0defg\\u1234 XXX \\uF8D2\\U0010FEDC')
    0
    >>> m_wide_unicode_literal_cascade_eq(ord('X'), 'abc\\0defg\\u1234\\uF8D2\\U0010FEDC')
    0
    >>> m_wide_unicode_literal_cascade_eq(ord(py_wide_unicode_character), 'abc\\0defg\\u1234\\uF8D2\\U0010FEDC')
    1
    """
    cdef int result = a in u'abc\0defg\u1234\uF8D2\U0010FEDC' == cascade
    return result


@cython.test_assert_path_exists("//SwitchStatNode", "//BoolBinopNode")
@cython.test_fail_if_path_exists("//PrimaryCmpNode")
def m_tuple_in_or_notin(int a):
    """
    >>> m_tuple_in_or_notin(2)
    0
    >>> m_tuple_in_or_notin(3)
    1
    >>> m_tuple_in_or_notin(5)
    1
    """
    cdef int result = a not in (1,2,3,4) or a in (3,4)
    return result

@cython.test_assert_path_exists("//SwitchStatNode", "//BoolBinopNode")
@cython.test_fail_if_path_exists("//PrimaryCmpNode")
def m_tuple_notin_or_notin(int a):
    """
    >>> m_tuple_notin_or_notin(2)
    1
    >>> m_tuple_notin_or_notin(6)
    1
    >>> m_tuple_notin_or_notin(4)
    0
    """
    cdef int result = a not in (1,2,3,4) or a not in (4,5)
    return result

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//BoolBinopNode", "//PrimaryCmpNode")
def m_tuple_notin_and_notin(int a):
    """
    >>> m_tuple_notin_and_notin(2)
    0
    >>> m_tuple_notin_and_notin(6)
    0
    >>> m_tuple_notin_and_notin(5)
    1
    """
    cdef int result = a not in (1,2,3,4) and a not in (6,7)
    return result

@cython.test_assert_path_exists("//SwitchStatNode", "//BoolBinopNode")
@cython.test_fail_if_path_exists("//PrimaryCmpNode")
def m_tuple_notin_and_notin_overlap(int a):
    """
    >>> m_tuple_notin_and_notin_overlap(2)
    0
    >>> m_tuple_notin_and_notin_overlap(4)
    0
    >>> m_tuple_notin_and_notin_overlap(5)
    1
    """
    cdef int result = a not in (1,2,3,4) and a not in (3,4)
    return result

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//BoolBinopNode", "//PrimaryCmpNode")
def conditional_int(int a):
    """
    >>> conditional_int(1)
    2
    >>> conditional_int(0)
    1
    >>> conditional_int(5)
    1
    """
    return 1 if a not in (1,2,3,4) else 2

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//BoolBinopNode", "//PrimaryCmpNode")
def conditional_object(int a):
    """
    >>> conditional_object(1)
    '2'
    >>> conditional_object(0)
    1
    >>> conditional_object(5)
    1
    """
    return 1 if a not in (1,2,3,4) else '2'

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//BoolBinopNode", "//PrimaryCmpNode")
def conditional_bytes(char a):
    """
    >>> conditional_bytes(ord('a'))
    '2'
    >>> conditional_bytes(ord('X'))
    1
    >>> conditional_bytes(0)
    1
    """
    return 1 if a not in b'abc' else '2'

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//BoolBinopNode", "//PrimaryCmpNode")
def conditional_unicode(Py_UNICODE a):
    """
    >>> conditional_unicode(ord('a'))
    '2'
    >>> conditional_unicode(ord('X'))
    1
    >>> conditional_unicode(0)
    1
    """
    return 1 if a not in u'abc' else '2'

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//BoolBinopNode", "//PrimaryCmpNode")
def conditional_none(int a):
    """
    >>> conditional_none(1)
    1
    >>> conditional_none(0)
    >>> conditional_none(5)
    """
    return None if a not in {1,2,3,4} else 1

def n(a):
    """
    >>> n('d *')
    0
    >>> n('xxx')
    1
    """
    cdef int result = a.lower() not in [u'a *',u'b *',u'c *',u'd *']
    return result

def p(a):
    """
    >>> p('a')
    0
    >>> p(1)
    1
    """
    cdef dict d = {u'a': 1, u'b': 2}
    cdef int result = a not in d
    return result

def q(a):
    """
    >>> q(1)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not iterable
    """
    cdef dict d = None
    cdef int result = a not in d # should fail with a TypeError
    return result


def p_frozendict(a):
    """
    >>> p_frozendict('a')
    0
    >>> p_frozendict(1)
    1
    """
    cdef frozendict fd = frozendict({u'a': 1, u'b': 2})
    cdef int result = a not in fd
    return result


def q_frozendict(a):
    """
    >>> q_frozendict(1)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not iterable
    """
    cdef frozendict fd = None
    cdef int result = a not in fd  # should fail with a TypeError
    return result
