# ticket: 431

__doc__ = u"""
>>> s == s_interned
True
>>> s == s_interned_dynamic
True
>>> s == 'abc' == s_interned == s_interned_dynamic
True
"""

import sys
if sys.version_info[0] < 3:
    __doc__ += u"""
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
