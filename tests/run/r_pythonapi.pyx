__doc__ = u"""
    >>> x = spam()
    >>> print(repr(x))
    u'Ftang\\x00Ftang!'
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u" u'", u" '")

cdef extern from "string.h":
    void memcpy(char *d, char *s, int n)

from cpython cimport PyUnicode_DecodeUTF8

def spam():
    cdef char[12] buf
    memcpy(buf, "Ftang\0Ftang!", sizeof(buf))
    return PyUnicode_DecodeUTF8(buf, sizeof(buf), NULL)
