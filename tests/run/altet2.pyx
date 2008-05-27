__doc__ = u"""
  >>> iter(C())
  Traceback (most recent call last):
  TypeError: iter() returned non-iterator of type 'NoneType'
"""

cdef class C:

    def __iter__(self):
        "This is a doc string."
