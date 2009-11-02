__doc__ = u"""
>>> try:
...     eggs().eat()
... except RuntimeError:
...    import sys
...    e = sys.exc_info()[1]
...    print("%s: %s" % (e.__class__.__name__, e))
RuntimeError: I don't like that
"""

cdef class eggs:

  def __dealloc__(self):
    pass

  def eat(self):
    raise RuntimeError(u"I don't like that")
