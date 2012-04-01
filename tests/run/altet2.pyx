__doc__ = u"""
  >>> iter(C())    # doctest: +ELLIPSIS
  Traceback (most recent call last):
  TypeError: iter() returned non-iterator...
"""

cdef class C:

    def __iter__(self):
        "This is a doc string."
