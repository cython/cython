__doc__ = u"""
    >>> f()
    >>> g
    42
    >>> x
    u'spam'
    >>> y
    u'eggs'
    >>> z
    u'spameggs'
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u" u'", u" '")

def f():
    pass
    
g = 42
x = u"spam"
y = u"eggs"
if g:
    z = x + y
