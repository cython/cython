#
#  Example of an extension type.
#

cdef class Spam:

  cdef int amount

  def __new__(self):
    self.amount = 0

  def __dealloc__(self):
    print self.amount, "tons of spam is history."

  def get_amount(self):
    return self.amount

  def set_amount(self, new_amount):
    self.amount = new_amount

  def describe(self):
    print self.amount, "tons of spam!"
