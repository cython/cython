# mode: compile

cdef i32 blarg(i32 i):
    pass

cdef void foo():
    let f32 f=0
    let i32 i
    if blarg(<i32> f):
        pass

foo()
