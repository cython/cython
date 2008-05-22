__doc__ = u"""
    >>> s = Spam() #doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: function takes exactly 3 arguments (0 given)
"""

import sys, re
if sys.version_info >= (2,6):
    __doc__ = re.sub(u"Error: .*", u"Error: ...", __doc__)

cdef class Spam:

    def __init__(self, a, b, int c):
        pass
