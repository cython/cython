__doc__ = u"""
>>> import sys
>>> if not IS_PY3: sys.exc_clear()

>>> def test_py():
...   try:
...     raise AttributeError
...   except AttributeError:
...     test_c(error=AttributeError)
...     print(sys.exc_info()[0] is AttributeError or sys.exc_info()[0])
...   print((IS_PY3 and sys.exc_info()[0] is TestException) or
...         (not IS_PY3 and sys.exc_info()[0] is AttributeError) or
...         sys.exc_info()[0])

>>> print(sys.exc_info()[0]) # 0
None
>>> test_py()
True
True
True
True

>>> print(sys.exc_info()[0]) # test_py()
None

>>> test_c(test_py)
True
True
True
True
True
True

>>> print(sys.exc_info()[0]) # test_c()
None
"""

import sys
IS_PY3 = sys.version_info[0] >= 3

class TestException(Exception):
    pass

def test_c(func=None, error=None):
    try:
        raise TestException
    except TestException:
        if func:
            func()
        print(sys.exc_info()[0] is TestException or sys.exc_info()[0])
    print(sys.exc_info()[0] is error or sys.exc_info()[0])
