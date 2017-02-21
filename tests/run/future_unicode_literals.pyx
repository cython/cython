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
    >>> raw ==  'abc\\\\xf8\\\\t\\u00f8\\U000000f8'  # unescaped by Python (required by doctest)
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
    >>> raw == u'abc\\\\xf8\\\\t\\u00f8\\U000000f8'  # unescaped by Python (required by doctest)
    True
"""

u = "test"

cdef char* s = "bytes test"
b = s

raw = r'abc\xf8\t\u00f8\U000000f8'
