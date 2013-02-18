# coding=utf-8
__doc__ = u"""
    >>> do_slice(u'abcdef', 2, 3)
    (u'c', u'cdef', u'ab', u'abcdef')
    >>> do_slice(u'abcdef', 0, 5)
    (u'abcde', u'abcdef', u'', u'abcdef')
"""

import sys

if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"(u'", u"('").replace(u" u'", u" '")

def do_slice(unicode s, int i, int j):
    return s[i:j], s[i:], s[:i], s[:]

