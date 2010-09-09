from __future__ import unicode_literals

import sys
if sys.version_info[0] >= 3:
    __doc__ = u"""
    >>> u == 'test'
    True
    >>> isinstance(u, str)
    True
    >>> isinstance(b, bytes)
    True
"""
else:
    __doc__ = u"""
    >>> u == u'test'
    True
    >>> isinstance(u, unicode)
    True
    >>> isinstance(b, str)
    True
"""

u = "test"

cdef char* s = "bytes test"
b = s
