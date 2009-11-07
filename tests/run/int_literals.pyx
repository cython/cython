__doc__ = u"""
>>> c_longs()
(1, 1L, -1L, 18446744073709551615L)
>>> py_longs()
(1, 1L, 100000000000000000000000000000000L, -100000000000000000000000000000000L)
"""

import sys

if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u'L', u'')

import sys

if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u'L', u'')

def c_longs():
    cdef long a = 1L
    cdef unsigned long ua = 1UL
    cdef long long aa = 0xFFFFFFFFFFFFFFFFLL
    cdef unsigned long long uaa = 0xFFFFFFFFFFFFFFFFULL
    
    return a, ua, aa, uaa
    
def py_longs():
    return 1, 1L, 100000000000000000000000000000000, -100000000000000000000000000000000
