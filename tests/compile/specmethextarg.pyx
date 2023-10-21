# mode: compile

cdef class Spam:
    cdef i32 eggs

    def __iadd__(self, Spam other):
        self.eggs = self.eggs +  other.eggs
