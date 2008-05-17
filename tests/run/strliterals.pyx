__doc__ = ur"""
    >>> s1
    b'abc\x11'
    >>> len(s1)
    4

    >>> s2
    b'abc\\x11'
    >>> len(s2)
    7

    >>> s3
    b'abc\\x11'
    >>> len(s3)
    7

    >>> s4
    b'abc\x11'
    >>> len(s4)
    4

    >>> s5
    b'abc\x11'
    >>> len(s5)
    4

    >>> s6
    b'abc\\x11'
    >>> len(s6)
    7

    >>> s7
    b'abc\\x11'
    >>> len(s7)
    7

    >>> s8
    b'abc\\x11'
    >>> len(s8)
    7

    >>> u1
    u'abc\x11'
    >>> len(u1)
    4

    >>> u2
    u'abc\x11'
    >>> len(u2)
    4

    >>> u3
    u'abc\\x11'
    >>> len(u3)
    7

    >>> u4
    u'abc\\x11'
    >>> len(u4)
    7

    >>> u5
    u'abc\\x11'
    >>> len(u5)
    7
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u" u'", u" '")
else:
    __doc__ = __doc__.replace(u" b'", u" '")

s1 = "abc\x11"
s2 = r"abc\x11"
s3 = R"abc\x11"
s4 = b"abc\x11"
s5 = B"abc\x11"
s6 = br"abc\x11"
s7 = Br"abc\x11"
s8 = bR"abc\x11"

u1 = u"abc\x11"
u2 = U"abc\x11"
u3 = ur"abc\x11"
u4 = Ur"abc\x11"
u5 = uR"abc\x11"
