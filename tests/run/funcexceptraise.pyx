__doc__ = u"""
>>> def bar():
...     try:
...         foo()
...     except ValueError:
...         pass

>>> bar()
>>> print(sys.exc_info())
(None, None, None)
"""

import sys

def foo():
    try:
        raise TypeError
    except TypeError:
        raise ValueError
