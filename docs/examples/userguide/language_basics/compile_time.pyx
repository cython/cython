DEF FavouriteFood = u"spam"
DEF ArraySize = 42
DEF OtherArraySize = 2 * ArraySize + 17

cdef int[ArraySize] a1
cdef int[OtherArraySize] a2
print("I like", FavouriteFood)
