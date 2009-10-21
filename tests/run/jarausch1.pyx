__doc__ = u"""
   >>> b == br'\\\\'
   True
   >>> s ==  r'\\\\'
   True
   >>> u == ur'\\\\'
   True
"""

import sys
if sys.version_info[0] < 3:
    __doc__ = __doc__.replace(u" br'", u" r'")
else:
    __doc__ = __doc__.replace(u" ur'", u" r'")

b = br'\\'
s =  r'\\'
u = ur'\\'
