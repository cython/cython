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
>>> s == 'a����o'
True

>>> isinstance(add(), str)
True
>>> len(add())
9
>>> add() == 'abca����o'
True

>>> isinstance(add_literal(), str)
True
>>> len(add_literal())
9
>>> add_literal() == 'abca����o'
True

>>> isinstance(typed(), str)
True
>>> len(typed())
6
>>> typed() == '������'
True

"""
# recoding/escaping is required to properly pass the literals to doctest
).encode('unicode_escape').decode('ASCII').replace(u'\\n', u'\n')

a = 'abc'
s = 'a����o'
u = u'a����o'

cdef str S = '������'

def add():
    return a+s

def add_literal():
    return 'abc' + 'a����o'

def typed():
    return S
