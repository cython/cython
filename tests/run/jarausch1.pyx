__doc__ = u"""
   >>> py_x = br'\\\\'
   >>> assert x == py_x
"""

import sys
if sys.version_info[0] < 3:
    __doc__ = __doc__.replace(u" br'", u" r'")

x = r'\\'
