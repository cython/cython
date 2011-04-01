# mode: compile

cdef void foo():
    cdef int bool, int1=0, int2=0
    bool = int1 < int2
    bool = int1 > int2
    bool = int1 <= int2
    bool = int1 >= int2

foo()
