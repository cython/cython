# mode: compile

cdef const_args(const int a, const int *b, const (int*) c, int *const d, int **const e, int *const *f):
    print a
    print b[0]
    b = NULL     # OK, the pointer itself is not const
    c[0] = 4     # OK, the value is not const
    d[0] = 7     # OK, the value is not const
    e[0][0] = 1  # OK, the value is not const
    e[0] = NULL  # OK, the pointed pointer is not const
    f[0][0] = 1  # OK, the value is not const
    f = NULL     # OK, the pointer is not const

def call_const_args(x):
    cdef int k = x
    cdef int* arr = [x]
    const_args(x, &k, &k, &k, &arr, &arr)
