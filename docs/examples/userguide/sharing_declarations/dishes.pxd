cdef enum OtherStuff:
    Sausage, Eggs, Lettuce

cdef struct SpamDish:
    i32 oz_of_spam
    OtherStuff filler
