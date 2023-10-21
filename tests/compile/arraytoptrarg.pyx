# mode: compile

cdef void f1(i8 *argv[]):
    f2(argv)

cdef void f2(i8 *argv[]):
    pass

f1(NULL)
