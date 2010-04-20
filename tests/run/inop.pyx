
cimport cython

def f(a,b):
    """
    >>> f(1,[1,2,3])
    True
    >>> f(5,[1,2,3])
    False
    >>> f(2,(1,2,3))
    True
    """
    cdef object result = a in b
    return result

def g(a,b):
    """
    >>> g(1,[1,2,3])
    1
    >>> g(5,[1,2,3])
    0
    >>> g(2,(1,2,3))
    1
    """
    cdef int result = a in b
    return result

def h(b):
    """
    >>> h([1,2,3,4])
    True
    >>> h([1,3,4])
    False
    """
    cdef object result = 2 in b
    return result

def j(b):
    """
    >>> j([1,2,3,4])
    1
    >>> j([1,3,4])
    0
    """
    cdef int result = 2 in b
    return result

@cython.test_fail_if_path_exists("//SwitchStatNode")
def k(a):
    """
    >>> k(1)
    1
    >>> k(5)
    0
    """
    cdef int result = a in [1,2,3,4]
    return result

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//PrimaryCmpNode")
def m_list(int a):
    """
    >>> m_list(2)
    1
    >>> m_list(5)
    0
    """
    cdef int result = a in [1,2,3,4]
    return result

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//PrimaryCmpNode")
def m_tuple(int a):
    """
    >>> m_tuple(2)
    1
    >>> m_tuple(5)
    0
    """
    cdef int result = a in (1,2,3,4)
    return result

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//PrimaryCmpNode")
def m_set(int a):
    """
    >>> m_set(2)
    1
    >>> m_set(5)
    0
    """
    cdef int result = a in {1,2,3,4}
    return result

cdef bytes bytes_string = b'abcdefg'
py_bytes_string = bytes_string

@cython.test_assert_path_exists("//PrimaryCmpNode")
@cython.test_fail_if_path_exists("//SwitchStatNode", "//BoolBinopNode")
def m_bytes(char a, bytes bytes_string):
    """
    >>> m_bytes(ord('f'), py_bytes_string)
    1
    >>> m_bytes(ord('X'), py_bytes_string)
    0
    >>> 'f'.encode('ASCII') in None
    Traceback (most recent call last):
    TypeError: argument of type 'NoneType' is not iterable
    >>> m_bytes(ord('f'), None)
    Traceback (most recent call last):
    TypeError: argument of type 'NoneType' is not iterable
    """
    cdef int result = a in bytes_string
    return result

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//PrimaryCmpNode")
def m_bytes_literal(char a):
    """
    >>> m_bytes_literal(ord('f'))
    1
    >>> m_bytes_literal(ord('X'))
    0
    """
    cdef int result = a in b'abcdefg'
    return result

cdef unicode unicode_string = u'abcdefg\u1234\uF8D2'
py_unicode_string = unicode_string

@cython.test_assert_path_exists("//PrimaryCmpNode")
@cython.test_fail_if_path_exists("//SwitchStatNode", "//BoolBinopNode")
def m_unicode(Py_UNICODE a, unicode unicode_string):
    """
    >>> m_unicode(ord('f'), py_unicode_string)
    1
    >>> m_unicode(ord('X'), py_unicode_string)
    0
    >>> 'f' in None
    Traceback (most recent call last):
    TypeError: argument of type 'NoneType' is not iterable
    >>> m_unicode(ord('f'), None)
    Traceback (most recent call last):
    TypeError: argument of type 'NoneType' is not iterable
    """
    cdef int result = a in unicode_string
    return result

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//PrimaryCmpNode")
def m_unicode_literal(Py_UNICODE a):
    """
    >>> m_unicode_literal(ord('f'))
    1
    >>> m_unicode_literal(ord('X'))
    0
    """
    cdef int result = a in u'abcdefg\u1234\uF8D2'
    return result

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//PrimaryCmpNode")
def conditional_int(int a):
    """
    >>> conditional_int(1)
    1
    >>> conditional_int(0)
    2
    >>> conditional_int(5)
    2
    """
    return 1 if a in (1,2,3,4) else 2

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//PrimaryCmpNode")
def conditional_object(int a):
    """
    >>> conditional_object(1)
    1
    >>> conditional_object(0)
    '2'
    >>> conditional_object(5)
    '2'
    """
    return 1 if a in (1,2,3,4) else '2'

@cython.test_assert_path_exists("//SwitchStatNode")
@cython.test_fail_if_path_exists("//BoolBinopNode", "//PrimaryCmpNode")
def conditional_none(int a):
    """
    >>> conditional_none(1)
    >>> conditional_none(0)
    1
    >>> conditional_none(5)
    1
    """
    return None if a in {1,2,3,4} else 1

def n(a):
    """
    >>> n('d *')
    1
    >>> n('xxx')
    0
    """
    cdef int result = a.lower() in [u'a *',u'b *',u'c *',u'd *']
    return result

def p(a):
    """
    >>> p(1)
    0
    >>> p('a')
    1
    """
    cdef dict d = {u'a': 1, u'b': 2}
    cdef int result = a in d
    return result

def q(a):
    """
    >>> q(1)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not iterable
        >>> l = [1,2,3,4]
    >>> l2 = [l[1:],l[:-1],l]
    >>> 2 in l in l2
    True
    """
    cdef dict d = None
    cdef int result = a in d # should fail with a TypeError
    return result

def r(a):
    """
    >>> r(2)
    1
    """
    cdef object l = [1,2,3,4]
    cdef object l2 = [l[1:],l[:-1],l]
    cdef int result = a in l in l2
    return result

def s(a):
    """
    >>> s(2)
    1
    """
    cdef int result = a in [1,2,3,4] in [[1,2,3],[2,3,4],[1,2,3,4]]
    return result
