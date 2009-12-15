#  -*- coding: latin-1 -*-

__doc__ = (u"""
>>> a == 'abc'
True
>>> isinstance(a, str)
True

>>> isinstance(s, str)
True
>>> len(s)
6
>>> s == 'aäÄÖöo'
True

>>> isinstance(add(), str)
True
>>> len(add())
9
>>> add() == 'abcaäÄÖöo'
True

>>> isinstance(add_literal(), str)
True
>>> len(add_literal())
9
>>> add_literal() == 'abcaäÄÖöo'
True

>>> isinstance(typed(), str)
True
>>> len(typed())
6
>>> typed() == 'üüääöö'
True

"""
# recoding/escaping is required to properly pass the literals to doctest
).encode('unicode_escape').decode('ASCII').replace(u'\\n', u'\n')

a = 'abc'
s = 'aäÄÖöo'
u = u'aäÄÖöo'

cdef str S = 'üüääöö'

def add():
    return a+s

def add_literal():
    return 'abc' + 'aäÄÖöo'

def typed():
    return S
