# mode: compile

cdef i32 blarg(i32 i):
    pass

cdef void foo():
    cdef f32 f=0
    cdef i32 i
    if blarg(<i32> f):
        pass

foo()
