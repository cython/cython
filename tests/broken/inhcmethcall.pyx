cdef class Parrot:

  cdef void describe(self):
    pass


cdef class Norwegian(Parrot):

  cdef void describe(self):
    Parrot.describe(self)
