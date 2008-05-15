__doc__ = u"""
    >>> s = Spam()
    Traceback (most recent call last):
    TypeError: function takes exactly 3 arguments (0 given)
"""

import sys, re
if sys.version_info[0] >= 3:
    __doc__ = re.sub(u"Error: (.*)exactly(.*)", u"Error: \\1at most\\2", __doc__)

cdef class Spam:

    def __init__(self, a, b, int c):
        pass
