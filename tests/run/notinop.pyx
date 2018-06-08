
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

cdef unicode unicode_string = u'abcdefg\u1234\uF8D2'
py_unicode_string = unicode_string

cdef unicode klingon_character = u'\uF8D2'
py_klingon_character = klingon_character

@cython.test_assert_path_exists("//PrimaryCmpNode")
@cython.test_fail_if_path_exists("//SwitchStatNode", "//BoolBinopNode", "//BoolBinopNode")
def m_unicode(Py_UNICODE a, unicode unicode_string):
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

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//BoolBinopNode", "//PrimaryCmpNode")
def m_unicode_literal(Py_UNICODE a):
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
