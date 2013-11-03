# coding: utf-8

__doc__ = u"""
    >>> slice_start_end(u'abcdef', 2, 3)
    c
    >>> slice_start(u'abcdef', 2, 3)
    cdef
    >>> slice_end(u'abcdef', 2, 3)
    ab
    >>> slice_all(u'abcdef', 2, 3)
    abcdef
    >>> slice_start_none(u'abcdef', 2, 3)
    cdef
    >>> slice_none_end(u'abcdef', 2, 3)
    ab
    >>> slice_none_none(u'abcdef', 2, 3)
    abcdef

    >>> slice_start_end(u'abcdef', 2, 10)
    cdef
    >>> slice_start(u'abcdef', 2, 10)
    cdef
    >>> slice_end(u'abcdef', 2, 10)
    ab
    >>> slice_all(u'abcdef', 2, 10)
    abcdef

    >>> slice_start_end(u'abcdef', 0, 5)
    abcde
    >>> slice_start(u'abcdef', 0, 5)
    abcdef
    >>> slice_end(u'abcdef', 0, 5)
    <BLANKLINE>
    >>> slice_all(u'abcdef', 0, 5)
    abcdef
    >>> slice_start_none(u'abcdef', 0, 5)
    abcdef
    >>> slice_none_end(u'abcdef', 0, 5)
    <BLANKLINE>
    >>> slice_none_none(u'abcdef', 0, 5)
    abcdef

    >>> slice_start_end(u'abcdef', -6, -1)
    abcde
    >>> slice_start(u'abcdef', -6, -1)
    abcdef
    >>> slice_end(u'abcdef', -6, -1)
    <BLANKLINE>
    >>> slice_all(u'abcdef', -6, -1)
    abcdef
    >>> slice_start_none(u'abcdef', -6, -1)
    abcdef
    >>> slice_none_end(u'abcdef', -6, -1)
    <BLANKLINE>
    >>> slice_none_none(u'abcdef', -6, -1)
    abcdef

    >>> slice_start_end(u'abcdef', -6, -7)
    <BLANKLINE>
    >>> slice_start(u'abcdef', -6, -7)
    abcdef
    >>> slice_end(u'abcdef', -6, -7)
    <BLANKLINE>
    >>> slice_all(u'abcdef', -6, -7)
    abcdef
    >>> slice_start_none(u'abcdef', -6, -7)
    abcdef
    >>> slice_none_end(u'abcdef', -6, -7)
    <BLANKLINE>
    >>> slice_none_none(u'abcdef', -6, -7)
    abcdef

    >>> slice_start_end(u'abcdef', -7, -7)
    <BLANKLINE>
    >>> slice_start(u'abcdef', -7, -7)
    abcdef
    >>> slice_end(u'abcdef', -7, -7)
    <BLANKLINE>
    >>> slice_all(u'abcdef', -7, -7)
    abcdef
    >>> slice_start_none(u'abcdef', -7, -7)
    abcdef
    >>> slice_none_end(u'abcdef', -7, -7)
    <BLANKLINE>
    >>> slice_none_none(u'abcdef', -7, -7)
    abcdef

    >>> slice_start_end(u'aАbБcСdДeЕfФ', 2, 8)
    bБcСdД
    >>> slice_start(u'aАbБcСdДeЕfФ', 2, 8)
    bБcСdДeЕfФ
    >>> slice_end(u'aАbБcСdДeЕfФ', 2, 8)
    aА
    >>> slice_all(u'aАbБcСdДeЕfФ', 2, 8)
    aАbБcСdДeЕfФ
    >>> slice_start_none(u'aАbБcСdДeЕfФ', 2, 8)
    bБcСdДeЕfФ
    >>> slice_none_end(u'aАbБcСdДeЕfФ', 2, 8)
    aА
    >>> slice_none_none(u'aАbБcСdДeЕfФ', 2, 8)
    aАbБcСdДeЕfФ

    >>> slice_start_end(u'АБСДЕФ', 2, 4)
    СД
    >>> slice_start(u'АБСДЕФ', 2, 4)
    СДЕФ
    >>> slice_end(u'АБСДЕФ', 2, 4)
    АБ
    >>> slice_all(u'АБСДЕФ', 2, 4)
    АБСДЕФ
    >>> slice_start_none(u'АБСДЕФ', 2, 4)
    СДЕФ
    >>> slice_none_end(u'АБСДЕФ', 2, 4)
    АБ
    >>> slice_none_none(u'АБСДЕФ', 2, 4)
    АБСДЕФ

    >>> slice_start_end(u'АБСДЕФ', -4, -2)
    СД
    >>> slice_start(u'АБСДЕФ', -4, -2)
    СДЕФ
    >>> slice_end(u'АБСДЕФ', -4, -2)
    АБ
    >>> slice_all(u'АБСДЕФ', -4, -2)
    АБСДЕФ
    >>> slice_start_none(u'АБСДЕФ', -4, -2)
    СДЕФ
    >>> slice_none_end(u'АБСДЕФ', -4, -2)
    АБ
    >>> slice_none_none(u'АБСДЕФ', -4, -2)
    АБСДЕФ

    >>> slice_start_end(None, 2, 4)
    Traceback (most recent call last):    
    TypeError: 'NoneType' object is not subscriptable
    >>> slice_start(None, 2, 4)
    Traceback (most recent call last):    
    TypeError: 'NoneType' object is not subscriptable
    >>> slice_end(None, 2, 4)
    Traceback (most recent call last):    
    TypeError: 'NoneType' object is not subscriptable
    >>> slice_all(None, 2, 4)
    Traceback (most recent call last):    
    TypeError: 'NoneType' object is not subscriptable
    >>> slice_start_none(None, 2, 4)
    Traceback (most recent call last):    
    TypeError: 'NoneType' object is not subscriptable
    >>> slice_none_end(None, 2, 4)
    Traceback (most recent call last):    
    TypeError: 'NoneType' object is not subscriptable
    >>> slice_none_none(None, 2, 4)
    Traceback (most recent call last):    
    TypeError: 'NoneType' object is not subscriptable
"""

import sys

if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"(u'", u"('").replace(u" u'", u" '")

def slice_start_end(unicode s, int i, int j):
    print(s[i:j])

def slice_start(unicode s, int i, int j):
    print(s[i:])

def slice_end(unicode s, int i, int j):
    print(s[:i])

def slice_all(unicode s, int i, int j):
    print(s[:])

def slice_start_none(unicode s, int i, int j):
    print(s[i:None])

def slice_none_end(unicode s, int i, int j):
    print(s[None:i])

def slice_none_none(unicode s, int i, int j):
    print(s[None:None])
