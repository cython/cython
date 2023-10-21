# mode: compile

cdef extern from *:
    cdef packed struct MyStruct:
        char a

cdef public packed struct PublicStruct:
    i32 a
    u8 b
    i32 c
