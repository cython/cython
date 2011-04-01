# tag: cpp
# mode: compile

cdef extern from "cpp_enums.h":
    cdef enum Enum1:
        Item1
        Item2

a = Item1
b = Item2

cdef Enum1 x, y
x = Item1
y = Item2

cdef extern from "cpp_enums.h" namespace "Namespace1":
    cdef enum Enum2:
        Item3
        Item4

c = Item3
d = Item4

cdef Enum2 z, w
z = Item3
w = Item4

