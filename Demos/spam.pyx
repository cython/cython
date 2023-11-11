# cython: language_level=3

#
#  Example of an extension type.
#

cdef class Spam:
    cdef public int amount

    def __cinit__(self):
        self.amount = 0

    def __dealloc__(self):
        print(self.amount, "tons of spam is history.")

    def get_amount(self):
        return self.amount

    def set_amount(self, new_amount):
        self.amount = new_amount

    def describe(self):
        print(self.amount, "tons of spam!")
