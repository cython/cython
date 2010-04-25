# -*- coding: iso-8859-1 -*-

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


def compare_KLINGON():
    """
    >>> compare_ASCII()
    True
    False
    False
    """
    print(char_KLINGON == u'\uF8D2')
    print(char_KLINGON == u'A')
    print(char_KLINGON == u'B')


def index_literal(int i):
    """
    >>> index_literal(0) == '1'
    True
    >>> index_literal(-5) == '1'
    True
    >>> index_literal(2) == '3'
    True
    >>> index_literal(4) == '5'
    True
    """
    return u"12345"[i]


def index_literal_pyunicode(int i):
    """
    >>> index_literal_pyunicode(0) == '1'
    True
    >>> index_literal_pyunicode(-5) == '1'
    True
    >>> index_literal_pyunicode(2) == '3'
    True
    >>> index_literal_pyunicode(4) == '5'
    True
    """
    return <Py_UNICODE>(u"12345"[i])


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
