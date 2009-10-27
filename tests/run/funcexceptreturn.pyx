__doc__ = u"""
>>> import sys
>>> if not IS_PY3: sys.exc_clear()

>>> print(sys.exc_info()[0]) # 0
None
>>> exc = test_c()
>>> isinstance(exc, TestException) or exc
True
>>> print(sys.exc_info()[0]) # test_c()
None
"""

import sys

IS_PY3 = sys.version_info[0] >= 3

class TestException(Exception):
    pass

def test_c():
    try:
        raise TestException
    except TestException, e:
        return e
