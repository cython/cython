__doc__ = u"""
>>> import sys

>>> def test_py():
...   try:
...     raise AttributeError
...   except AttributeError:
...     print(sys.exc_info()[0] == AttributeError or sys.exc_info()[0])
...   print(sys.exc_info()[0] is None  or  sys.exc_info()[0])

>>> print(sys.exc_info()[0]) # 0
None
>>> test_py()
True
True

>>> print(sys.exc_info()[0]) # test_py()
None

>>> test_c()
True
True
>>> print(sys.exc_info()[0]) # test_c()
None
"""

import sys


def test_c():
    try:
        raise AttributeError
    except AttributeError:
        print(sys.exc_info()[0] == AttributeError or sys.exc_info()[0])
    print(sys.exc_info()[0] is None or sys.exc_info()[0])
