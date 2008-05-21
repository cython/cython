__doc__ = u"""
>>> y
(b'1', b'2', b'3')
>>> x
b'1foo2foo3'
"""

import sys
if sys.version_info[0] < 3:
    __doc__ = __doc__.replace(u"b'", u"'")


y = ('1','2','3')

x = 'foo'.join(y)
