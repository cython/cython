__doc__ = """
try:
    eggs().eat()
except RuntimeError, e:
    print "%s: %s" % (e.__class__.__name__, e)
"""

cdef class eggs:

  def __dealloc__(self):
    pass

  def eat(self):
    raise RuntimeError("I don't like that")

