# mode: compile

cdef extern from *:
    cdef void foo(i32[])

    ctypedef i32 MyInt
    cdef void foo(MyInt[])

    struct MyStruct:
        pass
    cdef void bar(MyStruct[])

    ctypedef MyStruct* MyStructP
    cdef void baz(MyStructP[])

cdef struct OtherStruct:
    i32 a

a = sizeof(i32[23][34])
b = sizeof(OtherStruct[43])

DEF COUNT = 4
c = sizeof(i32[COUNT])
d = sizeof(OtherStruct[COUNT])
