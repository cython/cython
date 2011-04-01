# tag: py3

__doc__ = u"""
>>> test_xrange()
0
1
2
>>> test_range()
0
1
2

>>> test_long() == 12
True
>>> test_int() == 12
True
"""

# the builtins 'xrange' and 'long' are not available in Py3, but they
# can safely be replaced by 'range' and 'int' on that platform

import sys

IS_PY3 = sys.version_info[0] >= 3

def test_xrange():
    r = xrange(3)
    assert type(r) is xrange
    for i in r:
        print i

def test_range():
    r = range(3)
    assert (type(r) is range) if IS_PY3 else (type(r) is list)
    for i in r:
        print i

def test_long():
    long_val = long(12)
    assert type(long_val) is long
    return long_val

def test_int():
    int_val = int(12)
    assert type(int_val) is int
    return int_val
