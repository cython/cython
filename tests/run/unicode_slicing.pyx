# coding: utf-8

__doc__ = u"""
    >>> do_slice1(u'abcdef', 2, 3)
    u'c'
    >>> do_slice2(u'abcdef', 2, 3)
    u'cdef'
    >>> do_slice3(u'abcdef', 2, 3)
    u'ab'
    >>> do_slice4(u'abcdef', 2, 3)
    u'abcdef'
    >>> do_slice5(u'abcdef', 2, 3)
    u'cdef'
    >>> do_slice6(u'abcdef', 2, 3)
    u'ab'
    >>> do_slice7(u'abcdef', 2, 3)
    u'abcdef'
    >>> do_slice1(u'abcdef', 0, 5)
    u'abcde'
    >>> do_slice2(u'abcdef', 0, 5)
    u'abcdef'
    >>> do_slice3(u'abcdef', 0, 5)
    u''
    >>> do_slice4(u'abcdef', 0, 5)
    u'abcdef'
    >>> do_slice5(u'abcdef', 0, 5)
    u'abcdef'
    >>> do_slice6(u'abcdef', 0, 5)
    u''
    >>> do_slice7(u'abcdef', 0, 5)
    u'abcdef'
    >>> do_slice1(u'aАbБcСdДeЕfФ', 2, 8)
    u'bБcСdД'
    >>> do_slice2(u'aАbБcСdДeЕfФ', 2, 8)
    u'bБcСdДeЕfФ'
    >>> do_slice3(u'aАbБcСdДeЕfФ', 2, 8)
    u'aА'
    >>> do_slice4(u'aАbБcСdДeЕfФ', 2, 8)
    u'aАbБcСdДeЕfФ'
    >>> do_slice5(u'aАbБcСdДeЕfФ', 2, 8)
    u'bБcСdДeЕfФ'
    >>> do_slice6(u'aАbБcСdДeЕfФ', 2, 8)
    u'aА'
    >>> do_slice7(u'aАbБcСdДeЕfФ', 2, 8)
    u'aАbБcСdДeЕfФ'
    >>> do_slice1(u'АБСДЕФ', 2, 4)
    u'СД'
    >>> do_slice2(u'АБСДЕФ', 2, 4)
    u'СДЕФ'
    >>> do_slice3(u'АБСДЕФ', 2, 4)
    u'АБ'
    >>> do_slice4(u'АБСДЕФ', 2, 4)
    u'АБСДЕФ'
    >>> do_slice5(u'АБСДЕФ', 2, 4)
    u'СДЕФ'
    >>> do_slice6(u'АБСДЕФ', 2, 4)
    u'АБ'
    >>> do_slice7(u'АБСДЕФ', 2, 4)
    u'АБСДЕФ'
    >>> do_slice1(None, 2, 4)
    Traceback (most recent call last):    
    TypeError: 'NoneType' object is not subscriptable
    >>> do_slice2(None, 2, 4)
    Traceback (most recent call last):    
    TypeError: 'NoneType' object is not subscriptable
    >>> do_slice3(None, 2, 4)
    Traceback (most recent call last):    
    TypeError: 'NoneType' object is not subscriptable
    >>> do_slice4(None, 2, 4)
    Traceback (most recent call last):    
    TypeError: 'NoneType' object is not subscriptable
    >>> do_slice5(None, 2, 4)
    Traceback (most recent call last):    
    TypeError: 'NoneType' object is not subscriptable
    >>> do_slice6(None, 2, 4)
    Traceback (most recent call last):    
    TypeError: 'NoneType' object is not subscriptable
    >>> do_slice7(None, 2, 4)
    Traceback (most recent call last):    
    TypeError: 'NoneType' object is not subscriptable
"""

import sys

if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"(u'", u"('").replace(u" u'", u" '")
    ss = "'"
else:
    ss = "u'"

def do_slice1(unicode s, int i, int j):
    print(ss+s[i:j]+"'")

def do_slice2(unicode s, int i, int j):
    print(ss+s[i:]+"'")

def do_slice3(unicode s, int i, int j):
    print(ss+s[:i]+"'")

def do_slice4(unicode s, int i, int j):
    print(ss+s[:]+"'")

def do_slice5(unicode s, int i, int j):
    print(ss+s[i:None]+"'")

def do_slice6(unicode s, int i, int j):
    print(ss+s[None:i]+"'")

def do_slice7(unicode s, int i, int j):
    print(ss+s[None:None]+"'")
