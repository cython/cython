__doc__ = u"""
>>> p = Norwegian()
>>> p.describe()
Norwegian
Parrot
"""

cdef class Parrot:

  cdef void _describe(self):
    print u"Parrot"

  def describe(self):
    self._describe()

cdef class Norwegian(Parrot):

  cdef void _describe(self):
    print u"Norwegian"
    Parrot._describe(self)
