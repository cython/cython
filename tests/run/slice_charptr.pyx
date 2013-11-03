__doc__ = u"""
    >>> do_slice(b'abcdef', 2, 3)
    (b'c', b'cdef', b'ab', b'abcdef', b'cdef', b'ab', b'abcdef')
    >>> do_slice(b'abcdef', 0, 5)
    (b'abcde', b'abcdef', b'', b'abcdef', b'abcdef', b'', b'abcdef')
"""

import sys

if sys.version_info[0] < 3:
    __doc__ = __doc__.replace(u"(b'", u"('").replace(u" b'", u" '")

def do_slice(s, int i, int j):
    cdef char* ss = s
    return ss[i:j], ss[i:], ss[:i], ss[:], ss[i:None], ss[None:i], ss[None:None]

