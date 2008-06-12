__doc__ = u"""
    >>> print(D)
    {u'answer': (42, 42)}
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"u'", u"'")

D = {}

def foo(x):
    return x, x

cdef class Spam:
    answer = 42
    D[u'answer'] = foo(answer)
