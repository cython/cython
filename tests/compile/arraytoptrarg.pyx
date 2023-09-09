# mode: compile

cdef void f1(char *argv[]):
    f2(argv)

cdef void f2(char *argv[]):
    pass

f1(NULL)
