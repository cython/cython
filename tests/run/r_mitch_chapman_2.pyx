__doc__ = u"""
    >>> boolExpressionsFail()
    u'Not 2b'
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u" u'", u" '")

def boolExpressionsFail():
    dict = {1: 1}
    if not "2b" in dict:
        return u"Not 2b"
    else:
        return u"2b?"
