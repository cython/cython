# mode: compile

cdef extern from *:
    cdef packed struct MyStruct:
        char a

cdef public packed struct PublicStruct:
    int a
    unsigned char b
    int c
