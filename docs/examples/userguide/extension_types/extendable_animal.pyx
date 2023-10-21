cdef class Animal:
    cdef i32 number_of_legs

    def __init__(self, i32 number_of_legs):
        self.number_of_legs = number_of_legs

class ExtendableAnimal(Animal):  # Note that we use class, not cdef class
    pass

dog = ExtendableAnimal(4)
dog.has_tail = True
