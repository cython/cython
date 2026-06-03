@cython.cclass
class Animal:

    number_of_legs: cython.int
    __dict__: dict

    def __cinit__(self, number_of_legs: cython.int):
        self.number_of_legs = number_of_legs


dog = Animal(4)
dog.has_tail = True
