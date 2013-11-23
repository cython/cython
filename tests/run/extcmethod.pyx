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


def test_spam():
    """
    >>> test_spam()
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


cdef class SpamDish:
    cdef int spam

    cdef void describe(self):
        print "This dish contains", self.spam, "tons of spam."


cdef class FancySpamDish(SpamDish):
    cdef int lettuce

    cdef void describe(self):
        print "This dish contains", self.spam, "tons of spam",
        print "and", self.lettuce, "milligrams of lettuce."


cdef void describe_dish(SpamDish d):
    d.describe()


def test_spam_dish():
    """
    >>> test_spam_dish()
    This dish contains 42 tons of spam.
    This dish contains 88 tons of spam and 5 milligrams of lettuce.
    """
    cdef SpamDish s
    cdef FancySpamDish ss
    s = SpamDish()
    s.spam = 42
    ss = FancySpamDish()
    ss.spam = 88
    ss.lettuce = 5
    describe_dish(s)
    describe_dish(ss)
