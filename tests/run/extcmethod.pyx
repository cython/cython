# mode: run

cdef class Spam:

    cdef int tons

    cdef void add_tons(self, int x):
        self.tons += x

    cdef void eat(self):
        self.tons = 0

    def lift(self):
        print self.tons

cdef class SubSpam(Spam):

    cdef void add_tons(self, int x):
        self.tons += 2 * x

def test():
    """
    >>> test()
    5
    0
    20
    5
    """
    cdef Spam s
    cdef SubSpam ss
    s = Spam()
    s.eat()
    s.add_tons(5)
    s.lift()

    ss = SubSpam()
    ss.eat()
    ss.lift()

    ss.add_tons(10)
    ss.lift()

    s.lift()
