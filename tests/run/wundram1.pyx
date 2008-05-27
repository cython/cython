__doc__ = u"""
    >>> x
    5L
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"5L", u"5")

cdef unsigned int ui
ui = 5
x = ui
