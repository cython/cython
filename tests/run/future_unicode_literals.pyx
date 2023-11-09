from __future__ import unicode_literals

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

u = "test"

cdef char* s = "bytes test"
b = s

raw = r'abc\xf8\t\u00f8\U000000f8'
