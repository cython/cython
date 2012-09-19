# mode: compile

cdef const_args(const int a, const int *b, const (int*) c):
    print a
    print b[0]
    b = NULL    # OK, the pointer itself is not const
    c[0] = 4    # OK, the value is not const
