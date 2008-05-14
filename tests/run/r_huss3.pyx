__doc__ = u"""
>>> try:
...     foo()
... except Exception, e:
...     print "%s: %s" % (e.__class__.__name__, e)
ValueError: 
>>> try:
...     bar()
... except Exception, e:
...     print "%s: %s" % (e.__class__.__name__, e)
"""

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
