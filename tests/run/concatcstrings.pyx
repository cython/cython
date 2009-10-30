__doc__ = u"""
    >>> spam == u'C string 1' + u'C string 2'
    True
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u" u'", u" '")

spam = u"C string 1" + u"C string 2"
