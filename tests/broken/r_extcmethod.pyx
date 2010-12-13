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

def test():
    cdef SpamDish s
    cdef FancySpamDish ss
    s = SpamDish()
    s.spam = 42
    ss = FancySpamDish()
    ss.spam = 88
    ss.lettuce = 5
    describe_dish(s)
    describe_dish(ss)
