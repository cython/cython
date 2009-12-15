# -*- coding: utf-8 -*-

__doc__ = u"""
>>> len(u)
15
>>> default == 'abcdefg'.encode()
True
>>> isinstance(utf8, _bytes)
True
>>> utf8 == u.encode('UTF-8')
True
>>> isinstance(utf8_strict, _bytes)
True
>>> utf8_strict == u.encode('UTF-8', 'strict')
True
>>> isinstance(ascii_replace, _bytes)
True
>>> ascii_replace == u.encode('ASCII', 'replace')
True
>>> isinstance(cp850_strict, _bytes)
True
>>> cp850_strict == u.encode('cp850', 'strict')
True
>>> isinstance(latin1, _bytes)
True
>>> latin1 == u.encode('latin-1')
True
>>> isinstance(latin1_constant, _bytes)
True
>>> latin1_constant == latin1
True
"""

_bytes = bytes

cdef unicode text = u'abcäöüöéèâÁÀABC'

u = text

default = u'abcdefg'.encode()

utf8 = text.encode(u'UTF-8')

utf8_strict = text.encode(u'UTF-8', u'strict')

ascii_replace = text.encode(u'ASCII', u'replace')

cp850_strict = text.encode(u'cp850', u'strict')

latin1 = text.encode(u'latin-1')

latin1_constant = u'abcäöüöéèâÁÀABC'.encode('latin1')
