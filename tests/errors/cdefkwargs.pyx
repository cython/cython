__doc__ = u"""
    >>> call2()
    >>> call3()
    >>> call4()
"""

import sys, re
if sys.version_info >= (2,6):
    __doc__ = re.sub(u"Error: (.*)exactly(.*)", u"Error: \\1at most\\2", __doc__)

# the calls:

def call2():
    b(1,2)

def call3():
    b(1,2,3)

def call4():
    b(1,2,3,4)

# the called function:

cdef b(a, b, c=1, d=2):
    pass
