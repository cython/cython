
cimport cython

uspace = u' '
ustring_with_a = u'abcdefg'
ustring_without_a = u'bcdefg'

@cython.test_fail_if_path_exists('//SimpleCallNode')
def ord_Py_UNICODE(unicode s):
    """
    >>> ord_Py_UNICODE(uspace)
    32
    """
    cdef Py_UNICODE u
    u = s[0]
    return ord(u)

@cython.test_assert_path_exists('//IntNode')
@cython.test_fail_if_path_exists('//SimpleCallNode')
def ord_const():
    """
    >>> ord_const()
    32
    """
    return ord(u' ')

@cython.test_assert_path_exists('//PrimaryCmpNode//IntNode')
@cython.test_fail_if_path_exists('//SimpleCallNode')
def unicode_for_loop_ord(unicode s):
    """
    >>> unicode_for_loop_ord(ustring_with_a)
    True
    >>> unicode_for_loop_ord(ustring_without_a)
    False
    """
    for c in s:
        if ord(c) == ord(u'a'):
            return True
    return False
