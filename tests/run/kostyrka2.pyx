__doc__ = u"""
    >>> x = X()
    >>> x.slots
    [b'']
"""

import sys
if sys.version_info[0] < 3:
    __doc__ = __doc__.replace(u"b'", u"'")

class X:
        slots = ["", ]
