__doc__ = u"""
>>> import sys

>>> def test_py():
...   old_exc = sys.exc_info()[0]
...   try:
...     raise AttributeError("test")
...   except AttributeError:
...     test_c(error=AttributeError)
...     print(sys.exc_info()[0] is AttributeError or sys.exc_info()[0])
...   print((sys.exc_info()[0] is old_exc) or
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

>>> def test_raise():
...   raise TestException("test")
>>> test_catch(test_raise, TestException)
True
None
"""

import sys

class TestException(Exception):
    pass

def test_c(func=None, error=None):
    try:
        raise TestException(u"test")
    except TestException:
        if func:
            func()
        print(sys.exc_info()[0] is TestException or sys.exc_info()[0])
    print(sys.exc_info()[0] is error or sys.exc_info()[0])

def test_catch(func, error):
    try:
        func()
    except error:
        print(sys.exc_info()[0] is error or sys.exc_info()[0])
    print(sys.exc_info()[0] is error or sys.exc_info()[0])
