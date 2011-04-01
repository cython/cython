# tag: cpp
# mode: compile

cdef extern from "operators.h":
    cdef cppclass Operators:
        Operators(int)
        Operators operator+(Operators)
        Operators __add__(Operators, Operators)
        Operators __sub__(Operators, Operators)
        Operators __mul__(Operators, Operators)
        Operators __div__(Operators, Operators)
        bool __lt__(Operators, Operators)
        bool __le__(Operators, Operators)
        bool __eq__(Operators, Operators)
        bool __ne__(Operators, Operators)
        bool __gt__(Operators, Operators)
        bool __ge__(Operators, Operators)
        Operators __rshift__(Operators, int)
        Operators __lshift__(Operators, int)
        Operators __mod__(Operators, int)

cdef int v = 10
cdef Operators a
cdef Operators b
cdef Operators c

c = a + b
c = a - b
c = a * b
c = a / b
c = a << 2
c = a >> 1
c = b % 2
a < b
a <= b
a == b
a != b
a > b
a >= b

