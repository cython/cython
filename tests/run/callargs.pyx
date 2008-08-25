__doc__ = u"""
  >>> test_pos_args(h)
  1 2 3 * 0 0
  1 2 9 * 2 0
  1 2 7 * 2 0
  9 8 7 * 0 0
  7 8 9 * 0 0

  >>> test_kw_args(h)
  1 2 3 * 0 0
  1 2 9 * 2 1
  1 2 7 * 2 1
  1 2 9 * 2 2
  1 2 9 * 2 2
  1 2 9 * 2 3

  >>> test_kw_args(e)
  2 1
  5 1
  5 1
  5 2
  5 2
  5 3

  >>> test_kw(e)
  0 1
  0 2
  0 2
  0 1

  >>> test_kw(g)
  1
  2
  2
  1

  >>> test_pos_args(f)
  3
  5
  5
  3
  3

  >>> test_noargs(e)
  0 0
  >>> test_noargs(f)
  0
  >>> test_noargs(g)
  0

  # and some errors:

  >>> test_noargs(h)
  Traceback (most recent call last):
  TypeError: h() takes at least 3 positional arguments (0 given)

  >>> h(1,2, d=5)
  Traceback (most recent call last):
  TypeError: h() takes at least 3 positional arguments (2 given)
"""

def e(*args, **kwargs):
    print len(args), len(kwargs)

def f(*args):
    print len(args)

def g(**kwargs):
    print len(kwargs)

def h(a, b, c, *args, **kwargs):
    print a, b, c, u'*', len(args), len(kwargs)

args = (9,8,7)

import sys
if sys.version_info[0] >= 3:
    kwargs = {u"test" : u"toast"}
else:
    kwargs = {"test" : u"toast"}


def test_kw_args(f):
    f(1,2, c=3)
    f(1,2, d=3, *args)
    f(1,2, d=3, *(7,8,9))
    f(1,2, d=3, *args, **kwargs)
    f(1,2, d=3, *args, e=5)
    f(1,2, d=3, *args, e=5, **kwargs)

def test_pos_args(f):
    f(1,2,3)
    f(1,2, *args)
    f(1,2, *(7,8,9))
    f(*args)
    f(*(7,8,9))

def test_kw(f):
    f(c=3)
    f(d=3, e=5)
    f(d=3, **kwargs)
    f(**kwargs)

def test_noargs(f):
    f()
