__doc__ = u"""
  >>> test()
  1 2 3 * 0 0
  1 2 3 * 0 0
  1 2 9 * 2 1
  1 2 7 * 2 1
  1 2 9 * 2 2
  1 2 9 * 2 2
  1 2 9 * 2 3
"""

def f(a, b, c, *args, **kwargs):
    print a, b, c, u'*', len(args), len(kwargs)

args = (9,8,7)

import sys
if sys.version_info[0] >= 3:
    kwargs = {u"test" : u"toast"}
else:
    kwargs = {"test" : u"toast"}


def test():
    f(1,2,3)
    f(1,2, c=3)
    f(1,2, d=3, *args)
    f(1,2, d=3, *(7,8,9))
    f(1,2, d=3, *args, **kwargs)
    f(1,2, d=3, *args, e=5)
    f(1,2, d=3, *args, e=5, **kwargs)
