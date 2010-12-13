from b_extimpinherit cimport Parrot


cdef class Norwegian(Parrot):

    cdef action(self):
        print "This parrot is resting."

    cdef plumage(self):
        print "Lovely plumage!"


def main():
    cdef Parrot p
    cdef Norwegian n
    p = Parrot()
    n = Norwegian()
    print "Parrot:"
    p.describe()
    p.action()
    print "Norwegian:"
    n.describe()
    n.action()
    n.plumage()
