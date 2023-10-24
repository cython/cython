# mode: compile

extern from *:
    fn void foo(i32[])

    ctypedef i32 MyInt
    fn void foo(MyInt[])

    struct MyStruct:
        pass
    fn void bar(MyStruct[])

    ctypedef MyStruct* MyStructP
    fn void baz(MyStructP[])

struct OtherStruct:
    i32 a

a = sizeof(i32[23][34])
b = sizeof(OtherStruct[43])

DEF COUNT = 4
c = sizeof(i32[COUNT])
d = sizeof(OtherStruct[COUNT])
