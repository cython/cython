__doc__ = u"""
>>> try:
...     foo()
... except Exception, e:
...     print("%s: %s" % (e.__class__.__name__, e))
ValueError: 
>>> try:
...     bar()
... except Exception, e:
...     print("%s: %s" % (e.__class__.__name__, e))
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"Exception, e", u"Exception as e")

def bar():
    try:
        raise TypeError
    except TypeError:
        pass

def foo():
    try:
        raise ValueError
    except ValueError, e:
        bar()
        raise
