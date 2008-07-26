__doc__ = u"""
    >>> x = spam()
    >>> print(repr(x))
    b'Ftang\\x00Ftang!'
"""

import sys
if sys.version_info[0] < 3:
    __doc__ = __doc__.replace(u" b'", u" '")

cdef extern from "string.h":
    void memcpy(char *d, char *s, int n)

cdef extern from "Python.h":
    object PyString_FromStringAndSize(char *s, int len)
    
def spam():
    cdef char buf[12]
    memcpy(buf, "Ftang\0Ftang!", sizeof(buf))
    return PyString_FromStringAndSize(buf, sizeof(buf))
