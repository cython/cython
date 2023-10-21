# mode: compile

cdef class Spam:

    cdef i32 tons

    cdef void add_tons(self, i32 x):
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
