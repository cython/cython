cdef class Parrot:

    cdef object plumage

    def __init__(self):
        self.plumage = "yellow"

    def describe(self):
        print "This bird has lovely", self.plumage, "plumage."


cdef class Norwegian(Parrot):

    def __init__(self):
        self.plumage = "blue"

