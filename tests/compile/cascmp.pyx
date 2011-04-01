# mode: compile

cdef void foo():
    cdef int bool, int1=0, int2=0, int3=0, int4=0
    cdef object obj1, obj2, obj3, obj4
    obj1 = 1
    obj2 = 2
    obj3 = 3
    obj4 = 4
    bool = int1 < int2 < int3
    bool = obj1 < obj2 < obj3
    bool = int1 < int2 < obj3
    bool = obj1 < 2 < 3
    bool = obj1 < 2 < 3 < 4
    bool = int1 < (int2 == int3) < int4

foo()
