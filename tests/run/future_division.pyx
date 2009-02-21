from __future__ import division

__doc__ = u"""
>>> from future_division import doit
>>> doit(1,2)
(0.5, 0)
>>> doit(4,3)
(1.3333333333333333, 1)
>>> doit(4,3.0)
(1.3333333333333333, 1.0)
>>> doit(4,2)
(2.0, 2)
"""

def doit(x,y):
    return x/y, x//y
