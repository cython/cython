cdef class Parrot:

    cdef describe(self):
        print "This is a parrot."

    cdef action(self):
        print "Polly wants a cracker!"
