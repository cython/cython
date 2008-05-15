__doc__ = u"""
   >>> py_x = ur'\\\\'
   >>> assert x == py_x
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u" ur'", u" r'")

x = ur'\\'
