from __future__ import print_function

DEF FavouriteFood = u"spam"
DEF ArraySize = 42
DEF OtherArraySize = 2 * ArraySize + 17

cdef i32[ArraySize] a1
cdef i32[OtherArraySize] a2
print("I like", FavouriteFood)
