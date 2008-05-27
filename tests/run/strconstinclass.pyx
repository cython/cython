__doc__ = u"""
    >>> c = C()
    >>> c.x
    b'foo'
"""

import sys
if sys.version_info[0] < 3:
    __doc__ = __doc__.replace(u" b'", u" '")

class C:
    x = "foo"

