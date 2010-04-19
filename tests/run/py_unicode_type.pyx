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
    # runtime casts are not currently supported
    #return <Py_UNICODE>(u"12345"[i])
    return u"12345"[i]
