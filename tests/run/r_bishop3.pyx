__doc__ = u"""
>>> foo = Foo()
>>> fee = Fee()
>>> faa = Faa()
>>> fee.bof()
Fee bof 0
>>> faa.bof()
Foo bof 0
"""

cdef class Foo:
  cdef int val

  def __init__(self):
    self.val = 0


cdef class Fee(Foo):

  def bof(self):
    print 'Fee bof', self.val


cdef class Faa(Fee):

  def bof(self):
    print 'Foo bof', self.val
