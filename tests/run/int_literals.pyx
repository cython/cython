__doc__ = u"""
>>> c_longs()
(1, 1L, -1L, 18446744073709551615L)
>>> py_longs()
(1, 1L, 100000000000000000000000000000000L, -100000000000000000000000000000000L)
"""

import sys
from cython cimport typeof

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

def large_literal():
    """
    >>> type(large_literal()) is int
    True
    """
    if sys.version_info[0] >= 3 or sys.maxint > 0xFFFFFFFFFFFF:
        return 0xFFFFFFFFFFFF
    else:
        return 0xFFFFFFF

def c_long_types():
    """
    >>> c_long_types()
    long
    long
    long long
    unsigned long
    unsigned long
    unsigned long long
    """
    print typeof(1)
    print typeof(1L)
    print typeof(1LL)
    print typeof(1U)
    print typeof(1UL)
    print typeof(1ULL)
