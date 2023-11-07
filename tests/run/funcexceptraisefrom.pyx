__doc__ = u"""
>>> def bar():
...     try:
...         foo()
...     except ValueError:
...         print(isinstance(sys.exc_info()[1].__cause__, TypeError))

>>> bar()
True

>>> print(sys.exc_info())
(None, None, None)

>>> def bar2():
...     try:
...         foo2()
...     except ValueError:
...         cause = sys.exc_info()[1].__cause__
...         print(isinstance(cause, TypeError))
...         print(cause.args==('value',))
...         pass

>>> bar2()
True
True
"""

import sys

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

