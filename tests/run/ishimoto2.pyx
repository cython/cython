__doc__ = u"""
    >>> C().xxx(5)
    5
    >>> C().xxx()
    u'a b'
    >>> C().xxx(42)
    42
    >>> C().xxx()
    u'a b'
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u" u'", u" '")

class C:
    def xxx(self, p=u"a b"):
        return p
