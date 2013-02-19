# coding: utf-8

__doc__ = u"""
    >>> do_slice(u'abcdef', 2, 3)
    (u'c', u'cdef', u'ab', u'abcdef', u'cdef', u'ab', u'abcdef')
    >>> do_slice(u'abcdef', 0, 5)
    (u'abcde', u'abcdef', u'', u'abcdef', u'abcdef', u'', u'abcdef')
    >>> do_slice(u'aАbБcСdДeЕfФ', 2, 8)
    (u'bБcСdД', u'bБcСdДeЕfФ', u'aА', u'aАbБcСdДeЕfФ', u'bБcСdДeЕfФ', u'aА', u'aАbБcСdДeЕfФ')
    >>> do_slice(u'aАbБcСdДeЕfФ', 2, 8)
    (u'bБcСdД', u'bБcСdДeЕfФ', u'aА', u'aАbБcСdДeЕfФ', u'bБcСdДeЕfФ', u'aА', u'aАbБcСdДeЕfФ')
    >>> do_slice(u'АБСДЕФ', 2, 4)
    (u'СД', u'СДЕФ', u'АБ', u'АБСДЕФ', u'СДЕФ', u'АБ', u'АБСДЕФ')
    >>> do_slice(None, 2, 4)
    Traceback (most recent call last):    
    TypeError: 'NoneType' object is not slicable
"""

import sys

if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"(u'", u"('").replace(u" u'", u" '")

def do_slice(unicode s, int i, int j):
    return s[i:j], s[i:], s[:i], s[:], s[i:None], s[None:i], s[None:None]

