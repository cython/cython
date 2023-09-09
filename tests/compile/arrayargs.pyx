# mode: compile

cdef extern from *:

    cdef void foo(int[])

    ctypedef int MyInt
    cdef void foo(MyInt[])

    struct MyStruct:
        pass
    cdef void bar(MyStruct[])

    ctypedef MyStruct* MyStructP
    cdef void baz(MyStructP[])

cdef struct OtherStruct:
    int a

a = sizeof(int[23][34])
b = sizeof(OtherStruct[43])

DEF COUNT = 4
c = sizeof(int[COUNT])
d = sizeof(OtherStruct[COUNT])

