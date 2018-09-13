cdef class Animal:

    cdef int number_of_legs
    cdef dict __dict__

    def __cinit__(self, int number_of_legs):
        self.number_of_legs = number_of_legs


dog = Animal(4)
dog.has_tail = True
