# ticket: t431

__doc__ = u"""
>>> s == s_interned
True
>>> s == s_interned_dynamic
True
>>> s == 'abc' == s_interned == s_interned_dynamic
True
"""


s = 'abc'

s_interned = intern(s)

s_interned_dynamic = intern('a'+'b'+'c')
