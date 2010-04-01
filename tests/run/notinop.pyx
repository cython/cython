
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
@cython.test_fail_if_path_exists("//BoolBinopNode", "//PrimaryCmpNode")
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
