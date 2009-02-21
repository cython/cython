from __future__ import unicode_literals

import sys
if sys.version_info[0] >= 3:
    __doc__ = u"""
    >>> u == 'test'
    True
    >>> isinstance(u, str)
    True
"""
else:
    __doc__ = u"""
    >>> u == u'test'
    True
    >>> isinstance(u, unicode)
    True
"""

u = "test"
