# -*- coding: utf-8 -*-

import sys

__doc__ = br"""
    >>> sa
    'abc'
    >>> ua
    'abc'
    >>> b
    '123'
    >>> c
    'S\xf8k ik'
    >>> d
    '\xfc\xd6\xe4'
    >>> e
    '\x03g\xf8\uf8d2S\xf8k ik'
    >>> f
    '\xf8'
    >>> g
    '\udc00'
    >>> h
    '\ud800'
    >>> q
    '\udc00\ud800'

    # The output of surrogate pairs differs between 16/32bit Unicode runtimes.
    #>>> p
    #u'\ud800\udc00'

    >>> add
    'S\xf8k ik\xfc\xd6\xe4abc'
    >>> null
    '\x00'
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
    >>> len(q)
    2
    >>> len(q)
    2
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
    >>> ua ==  'abc'
    True
    >>> b ==  '123'
    True
    >>> c ==  'Søk ik'
    True
    >>> d ==  'üÖä'
    True
    >>> e ==  '\x03\x67\xf8\uf8d2Søk ik'     # unescaped by Cython
    True
    >>> e ==  '\\x03\\x67\\xf8\\uf8d2Søk ik' # unescaped by Python
    True
    >>> f ==  '\xf8'  # unescaped by Cython
    True
    >>> f ==  '\\xf8' # unescaped by Python
    True
    >>> g ==  '\\udc00' # unescaped by Python (required by doctest)
    True
    >>> h ==  '\\ud800' # unescaped by Python (required by doctest)
    True
    >>> p == (u'\\ud800\\udc00' if sys.maxunicode == 1114111 else  '\\U00010000')  or  p  # unescaped by Python (required by doctest)
    True
    >>> q ==  '\\udc00\\ud800'  or  q  # unescaped by Python (required by doctest)
    True
    >>> k ==  '\\N{SNOWMAN}' ==  '\\u2603'  or  k
    True
    >>> m ==  'abc\\\\xf8\\\\t\\u00f8\\U000000f8'  or  m  # unescaped by Python (required by doctest)
    True
    >>> add ==  'Søk ik' +  'üÖä' + 'abc'  or  add
    True
    >>> null ==  '\\x00' # unescaped by Python (required by doctest)
    True
    >>> wide_literal ==  '\\U00101234'   # unescaped by Python
    True
    >>> ustring_in_constant_tuple == ('a',  'abc',  '\\N{SNOWMAN}',  'x' * 3,  '\\N{SNOWMAN}' * 4 +  'O')  or  ustring_in_constant_tuple  # unescaped by Python
    True

    >>> expected =  '\U00101234'    # unescaped by Cython
    >>> if wide_literal == expected: print(True)
    ... else: print(repr(wide_literal), repr(expected), sys.maxunicode)
    True
"""

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
p = u'\ud800\udc00'  # surrogate pair
q = u'\udc00\ud800'  # reversed surrogate pair

add = u'Søk ik' + u'üÖä' + u'abc'
null = u'\x00'

wide_literal = u'\U00101234'

ustring_in_constant_tuple = ('a', u'abc', u'\N{SNOWMAN}', u'x' * 3, u'\N{SNOWMAN}' * 4 + u'O')
