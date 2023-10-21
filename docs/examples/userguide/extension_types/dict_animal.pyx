cdef class Animal:
    cdef i32 number_of_legs
    cdef dict __dict__

    def __init__(self, i32 number_of_legs):
        self.number_of_legs = number_of_legs


dog = Animal(4)
dog.has_tail = True
