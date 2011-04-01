# mode: compile

cdef class Spam:
    cdef int eggs

    def __iadd__(self, Spam other):
        self.eggs = self.eggs +  other.eggs

