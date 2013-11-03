# mode: compile

cdef const_args(const int a, const int *b, const (int*) c, int *const d):
    print a
    print b[0]
    b = NULL    # OK, the pointer itself is not const
    c[0] = 4    # OK, the value is not const
    d[0] = 7    # OK, the value is not const

def call_const_args(x):
    cdef int k = x
    const_args(x, &k, &k, &k)
