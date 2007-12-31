cdef class Spam:

    cdef int tons
    
    cdef void add_tons(self, int x):
        self.tons = self.tons + x

    cdef void eat(self):
        self.tons = 0


cdef class SuperSpam(Spam):

    cdef void add_tons(self, int x):
        self.tons = self.tons + 2 * x
