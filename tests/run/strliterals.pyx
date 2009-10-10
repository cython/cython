__doc__ = ur"""
    >>> s1
    'abc\x11'
    >>> s1 == 'abc\x11'
    True
    >>> len(s1)
    4

    >>> s2
    'abc\\x11'
    >>> s2 == r'abc\x11'
    True
    >>> len(s2)
    7

    >>> s3
    'abc\\x11'
    >>> s3 == R'abc\x11'
    True
    >>> len(s3)
    7

    >>> s4
    b'abc\x11'
    >>> s4 == b'abc\x11'
    True
    >>> len(s4)
    4

    >>> s5
    b'abc\x11'
    >>> s5 == B'abc\x11'
    True
    >>> len(s5)
    4

    >>> s6
    b'abc\\x11'
    >>> s6 == br'abc\x11'
    True
    >>> len(s6)
    7

    >>> s7
    b'abc\\x11'
    >>> s7 == Br'abc\x11'
    True
    >>> len(s7)
    7

    >>> s8
    b'abc\\x11'
    >>> s8 == bR'abc\x11'
    True
    >>> len(s8)
    7

    >>> s9
    b'abc\\x11'
    >>> s9 == BR'abc\x11'
    True
    >>> len(s9)
    7

    >>> u1
    u'abc\x11'
    >>> u1 == u'abc\x11'
    True
    >>> len(u1)
    4

    >>> u2
    u'abc\x11'
    >>> u2 == U'abc\x11'
    True
    >>> len(u2)
    4

    >>> u3
    u'abc\\x11'
    >>> u3 == ur'abc\x11'
    True
    >>> len(u3)
    7

    >>> u4
    u'abc\\x11'
    >>> u4 == Ur'abc\x11'
    True
    >>> len(u4)
    7

    >>> u5
    u'abc\\x11'
    >>> u5 == uR'abc\x11'
    True
    >>> len(u5)
    7

    >>> u6
    u'abc\\x11'
    >>> u6 == UR'abc\x11'
    True
    >>> len(u6)
    7
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u" u'", u" '").replace(u" U'", u" '").replace(u" ur'", u" r'").replace(u" uR'", u" R'").replace(u" Ur'", u" r'").replace(u" UR'", u" R'")
else:
    __doc__ = __doc__.replace(u" b'", u" '").replace(u" B'", u" '").replace(u" br'", u" r'").replace(u" bR'", u" R'").replace(u" Br'", u" r'").replace(u" BR'", u" R'")

s1 = "abc\x11"
s2 = r"abc\x11"
s3 = R"abc\x11"
s4 = b"abc\x11"
s5 = B"abc\x11"
s6 = br"abc\x11"
s7 = Br"abc\x11"
s8 = bR"abc\x11"
s9 = BR"abc\x11"

u1 = u"abc\x11"
u2 = U"abc\x11"
u3 = ur"abc\x11"
u4 = Ur"abc\x11"
u5 = uR"abc\x11"
u6 = UR"abc\x11"
