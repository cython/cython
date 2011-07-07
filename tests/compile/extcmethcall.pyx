# mode: compile

cdef class Spam:

    cdef int tons

    cdef void add_tons(self, int x):
        pass


cdef class SuperSpam(Spam):
    pass


cdef void tomato():
    cdef Spam spam
    cdef SuperSpam superspam = SuperSpam()
    spam = superspam
    spam.add_tons(42)
    superspam.add_tons(1764)

tomato()
