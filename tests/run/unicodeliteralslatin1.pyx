# -*- coding: latin-1 -*-

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
    >>> len(add)
    12
    >>> len(null)
    1
""".decode("ASCII") + u"""
    >>> ua == 'abc'
    True
    >>> b == '123'
    True
    >>> c == 'Søk ik'
    True
    >>> d == 'üÖä'
    True
    >>> e == '\x03\x67\xf8\uf8d2Søk ik'     # unescaped by Cython
    True
    >>> e == '\\x03\\x67\\xf8\\uf8d2Søk ik' # unescaped by Python
    True
    >>> f == '\xf8'  # unescaped by Cython
    True
    >>> f == '\\xf8' # unescaped by Python
    True
    >>> k == 'ä' == '\\N{LATIN SMALL LETTER A WITH DIAERESIS}'
    True
    >>> add == 'Søk ik' + 'üÖä' + 'abc'
    True
    >>> null == '\\x00' # unescaped by Python (required by doctest)
    True
"""

sa = 'abc'
ua = u'abc'

b = u'123'
c = u'Søk ik'
d = u'üÖä'
e = u'\x03\x67\xf8\uf8d2Søk ik'
f = u'\xf8'
k = u'\N{LATIN SMALL LETTER A WITH DIAERESIS}'

add = u'Søk ik' + u'üÖä' + u'abc'
null = u'\x00'
