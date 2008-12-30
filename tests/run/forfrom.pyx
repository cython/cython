__doc__ = u"""
>>> for_else()
30
>>> print( u'*'.join(int_comp()) )
00*01*02
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u" u'", u" '").replace(u' u"', u' "')

def for_else():
    cdef int i, j=0, k=2
    for i from 0 <= i < 10:
        j += k
    else:
        k = j+10
    return k

def int_comp():
    cdef int i
    return tuple([ u"%02d" % i
                   for i from 0 <= i < 3 ])
