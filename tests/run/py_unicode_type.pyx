# -*- coding: iso-8859-1 -*-

cimport cython

cdef Py_UNICODE char_ASCII = u'A'
cdef Py_UNICODE char_KLINGON = u'\uF8D2'

def compare_ASCII():
    """
    >>> compare_ASCII()
    True
    False
    False
    """
    print(char_ASCII == u'A')
    print(char_ASCII == u'B')
    print(char_ASCII == u'\uF8D2')


def compare_klingon():
    """
    >>> compare_klingon()
    True
    False
    False
    """
    print(char_KLINGON == u'\uF8D2')
    print(char_KLINGON == u'A')
    print(char_KLINGON == u'B')


from cpython.unicode cimport PyUnicode_FromOrdinal
import sys

u0 = u'\x00'
u1 = u'\x01'
umax = PyUnicode_FromOrdinal(sys.maxunicode)

def unicode_ordinal(Py_UNICODE i):
    """
    >>> ord(unicode_ordinal(0)) == 0
    True
    >>> ord(unicode_ordinal(1)) == 1
    True
    >>> ord(unicode_ordinal(sys.maxunicode)) == sys.maxunicode
    True

    >>> ord(unicode_ordinal(u0)) == 0
    True
    >>> ord(unicode_ordinal(u1)) == 1
    True
    >>> ord(unicode_ordinal(umax)) == sys.maxunicode
    True

    Value too small:
    >>> unicode_ordinal(-1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: ...

    Value too large:
    >>> unicode_ordinal(sys.maxunicode+1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: ...

    Less than one character:
    >>> unicode_ordinal(u0[:0])
    Traceback (most recent call last):
    ...
    ValueError: only single character unicode strings can be converted to Py_UNICODE, got length 0

    More than one character:
    >>> unicode_ordinal(u0+u1)
    Traceback (most recent call last):
    ...
    ValueError: only single character unicode strings can be converted to Py_UNICODE, got length 2
    """
    return i

@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists('//SimpleCallNode')
def unicode_type_methods(Py_UNICODE uchar):
    """
    >>> unicode_type_methods(ord('A'))
    [True, True, False, False, False, False, False, True, True]
    >>> unicode_type_methods(ord('a'))
    [True, True, False, False, True, False, False, False, False]
    >>> unicode_type_methods(ord('8'))
    [True, False, True, True, False, True, False, False, False]
    >>> unicode_type_methods(ord('\\t'))
    [False, False, False, False, False, False, True, False, False]
    """
    return [
        # character types
        uchar.isalnum(),
        uchar.isalpha(),
        uchar.isdecimal(),
        uchar.isdigit(),
        uchar.islower(),
        uchar.isnumeric(),
        uchar.isspace(),
        uchar.istitle(),
        uchar.isupper(),
        ]

@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists('//SimpleCallNode')
def unicode_methods(Py_UNICODE uchar):
    """
    >>> unicode_methods(ord('A')) == ['a', 'A', 'A']
    True
    >>> unicode_methods(ord('a')) == ['a', 'A', 'A']
    True
    """
    return [
        # character conversion
        uchar.lower(),
        uchar.upper(),
        uchar.title(),
        ]
