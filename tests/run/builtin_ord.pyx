
cimport cython

import sys

uspace = u' '
ustring_with_a = u'abcdefg'
ustring_without_a = u'bcdefg'


@cython.test_assert_path_exists(
    # ord() should receive and return a C value
    '//ReturnStatNode//CoerceToPyTypeNode//SimpleCallNode')
@cython.test_fail_if_path_exists(
    '//ReturnStatNode//SimpleCallNode//CoerceToPyTypeNode')
def ord_Py_UNICODE(unicode s):
    """
    >>> ord_Py_UNICODE(uspace)
    32
    """
    cdef Py_UNICODE u
    u = s[0]
    return ord(u)


@cython.test_assert_path_exists('//TupleNode//IntNode')
@cython.test_fail_if_path_exists('//SimpleCallNode')
def ord_const():
    """
    >>> ord(b' ')
    32
    >>> ord(' ')
    32
    >>> ord_const()
    (32, 32, 32, 255, 255, 4660, 0)
    """
    return ord(u' '), ord(b' '), ord(' '), ord('\xff'), ord(b'\xff'), ord(u'\u1234'), ord('\0')


@cython.test_assert_path_exists('//PrimaryCmpNode//IntNode')
#@cython.test_fail_if_path_exists('//SimpleCallNode')
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


def compare_to_char(s):
    """
    >>> compare_to_char(uspace)
    False
    >>> compare_to_char(b'a')
    False
    >>> compare_to_char(b'x')
    True
    >>> compare_to_char('x')
    True
    """
    cdef char c = b'x'
    return ord(s) == c


def ord_object(s):
    """
    >>> try: ord_object('abc')
    ... except ValueError: pass
    ... except TypeError: print("FAILED!")
    >>> ord_object('a')
    97
    >>> ord_object(b'a')
    97
    """
    return ord(s)


def non_builtin_ord(s):
    """
    >>> non_builtin_ord('x')
    (123, 123)
    """
    def _ord(s):
        return 123

    ord = _ord
    return ord(s), _ord(s)
