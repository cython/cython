__doc__ = u"""
>>> import sys

>>> print(sys.exc_info()[0]) # 0
None
>>> exc = test_c()
>>> isinstance(exc, TestException) or exc
True
>>> print(sys.exc_info()[0]) # test_c()
None
"""

import sys


class TestException(Exception):
    pass

def test_c():
    try:
        raise TestException
    except TestException, e:
        return e
