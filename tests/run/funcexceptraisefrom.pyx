__doc__ = u"""
>>> def bar():
...     try:
...         foo()
...     except ValueError:
...         if IS_PY3:
...             print(isinstance(sys.exc_info()[1].__cause__, TypeError))
...         else:
...             print(True)

>>> bar()
True

>>> print(sys.exc_info())
(None, None, None)

>>> def bar2():
...     try:
...         foo2()
...     except ValueError:
...         if IS_PY3:
...             cause = sys.exc_info()[1].__cause__
...             print(isinstance(cause, TypeError))
...             print(cause.args==('value',))
...             pass
...         else:
...             print(True)
...             print(True)

>>> bar2()
True
True
"""

import sys
IS_PY3 = sys.version_info[0] >= 3
if not IS_PY3:
    sys.exc_clear()

def foo():
    try:
        raise TypeError
    except TypeError:
        raise ValueError from TypeError

def foo2():
    try:
        raise TypeError
    except TypeError:
        raise ValueError() from TypeError('value')

