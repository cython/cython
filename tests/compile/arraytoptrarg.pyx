# mode: compile
# tag: test_in_limited_api

cdef void f1(char *argv[]):
    f2(argv)

cdef void f2(char *argv[]):
    pass

f1(NULL)
