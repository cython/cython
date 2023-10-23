__doc__ = u"""
    >>> test()
    This parrot is resting.
    Lovely plumage!
"""


cdef class Parrot:
    fn void describe(self):
        print u"This parrot is resting."

    def describe_python(self):
        self.describe()

cdef class Norwegian(Parrot):
    fn void describe(self):
        print u"Lovely plumage!"

def test():
    let Parrot p1, p2
    p1 = Parrot()
    p2 = Norwegian()
    p1.describe()
    p2.describe()
