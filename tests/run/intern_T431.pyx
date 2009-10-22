__doc__ = u"""
>>> s == s_interned
True
>>> intern(s) is s_interned
True
>>> intern('abc') is s_interned
True
>>> intern('abc') is s_interned_dynamic
True
"""

s = 'abc'

s_interned = intern(s)

s_interned_dynamic = intern('a'+'b'+'c')
