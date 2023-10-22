# mode: compile

cdef const_args(const i32 a, const i32 *b, const (i32*) c, i32 *const d, i32 **const e, i32 *const *f):
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
    let i32 k = x
    let i32* arr = [x]
    const_args(x, &k, &k, &k, &arr, &arr)
