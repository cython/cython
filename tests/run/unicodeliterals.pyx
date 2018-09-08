# -*- coding: utf-8 -*-

import sys

__doc__ = br"""
    >>> sa
    'abc'
    >>> ua
    u'abc'
    >>> b
    u'123'
    >>> c
    u'S\xf8k ik'
    >>> d
    u'\xfc\xd6\xe4'
    >>> e
    u'\x03g\xf8\uf8d2S\xf8k ik'
    >>> f
    u'\xf8'
    >>> g
    u'\udc00'
    >>> h
    u'\ud800'
    >>> add
    u'S\xf8k ik\xfc\xd6\xe4abc'
    >>> null
    u'\x00'
""".decode("ASCII") + b"""
    >>> len(sa)
    3
    >>> len(ua)
    3
    >>> len(b)
    3
    >>> len(c)
    6
    >>> len(d)
    3
    >>> len(e)
    10
    >>> len(f)
    1
    >>> len(g)
    1
    >>> len(h)
    1
    >>> len(add)
    12
    >>> len(null)
    1
    >>> sys.maxunicode >= 65535
    True
    >>> sys.maxunicode == 65535 and 1 or len(wide_literal) # test for wide build
    1
    >>> sys.maxunicode > 65535 and 2 or len(wide_literal)  # test for narrow build
    2
""".decode("ASCII") + u"""
    >>> ua == u'abc'
    True
    >>> b == u'123'
    True
    >>> c == u'Søk ik'
    True
    >>> d == u'üÖä'
    True
    >>> e == u'\x03\x67\xf8\uf8d2Søk ik'     # unescaped by Cython
    True
    >>> e == u'\\x03\\x67\\xf8\\uf8d2Søk ik' # unescaped by Python
    True
    >>> f == u'\xf8'  # unescaped by Cython
    True
    >>> f == u'\\xf8' # unescaped by Python
    True
    >>> g == u'\\udc00' # unescaped by Python (required by doctest)
    True
    >>> h == u'\\ud800' # unescaped by Python (required by doctest)
    True
    >>> k == u'\\N{SNOWMAN}' == u'\\u2603'
    True
    >>> m == u'abc\\\\xf8\\\\t\\u00f8\\U000000f8'  # unescaped by Python (required by doctest)
    True
    >>> add == u'Søk ik' + u'üÖä' + 'abc'
    True
    >>> null == u'\\x00' # unescaped by Python (required by doctest)
    True
    >>> wide_literal == u'\\U00101234'   # unescaped by Python
    True
    >>> ustring_in_constant_tuple == ('a', u'abc', u'\\N{SNOWMAN}', u'x' * 3, u'\\N{SNOWMAN}' * 4 + u'O')  or  ustring_in_constant_tuple  # unescaped by Python
    True
"""

if sys.version_info >= (2,6,5):
    # this doesn't work well in older Python versions
    __doc__ += u"""\
    >>> expected = u'\U00101234'    # unescaped by Cython
    >>> if wide_literal == expected: print(True)
    ... else: print(repr(wide_literal), repr(expected), sys.maxunicode)
    True
"""

if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u" u'", u" '")
else:
    __doc__ = __doc__.replace(u" b'", u" '")

sa = 'abc'
ua = u'abc'

b = u'123'
c = u'Søk ik'
d = u'üÖä'
e = u'\x03\x67\xf8\uf8d2Søk ik'
f = u'\xf8'
g = u'\udc00'   # lone trail surrogate
h = u'\ud800'   # lone lead surrogate
k = u'\N{SNOWMAN}'
m = ur'abc\xf8\t\u00f8\U000000f8'

add = u'Søk ik' + u'üÖä' + u'abc'
null = u'\x00'

wide_literal = u'\U00101234'

ustring_in_constant_tuple = ('a', u'abc', u'\N{SNOWMAN}', u'x' * 3, u'\N{SNOWMAN}' * 4 + u'O')
