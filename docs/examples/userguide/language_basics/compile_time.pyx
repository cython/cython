from __future__ import print_function

DEF FavouriteFood = u"spam"
DEF ArraySize = 42
DEF OtherArraySize = 2 * ArraySize + 17

cdef int a1[ArraySize]
cdef int a2[OtherArraySize]
print("I like", FavouriteFood)