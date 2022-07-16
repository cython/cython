@cython.cclass
class Animal:

    number_of_legs: cython.int

    def __cinit__(self, number_of_legs: cython.int):
        self.number_of_legs = number_of_legs


class ExtendableAnimal(Animal):  # Note that we use class, not cdef class
    pass


dog = ExtendableAnimal(4)
dog.has_tail = True
