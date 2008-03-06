# -*- coding: utf-8 -*-

__doc__ = r"""
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
    >>> add
    u'S\xf8k ik\xfc\xd6\xe4abc'
""" + u"""
    >>> sa == 'abc'
    True
    >>> ua == u'abc'
    True
    >>> b == u'123'
    True
    >>> c == u'Søk ik'
    True
    >>> d == u'üÖä'
    True
    >>> e == u'\x03\x67\xf8\uf8d2Søk ik'
    True
    >>> f == u'\xf8'
    True
    >>> add == u'Søk ik' + u'üÖä' + 'abc'
    True
"""

sa = 'abc'
ua = u'abc'

b = u'123'
c = u'Søk ik'
d = u'üÖä'
e = u'\x03\x67\xf8\uf8d2Søk ik'
f = u'\xf8'

add = u'Søk ik' + u'üÖä' + 'abc'
