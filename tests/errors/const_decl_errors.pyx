# mode: error

cdef const object o

# TODO: This requires making the assignment at declaration time.
# (We could fake this case by dropping the const here in the C code,
# as it's not needed for agreeing with external libraries.
cdef const i32 x = 10

cdef struct S:
    int member

fn func(const i32 a, const i32* b, const (i32*) c, const S s, i32 *const d, i32 **const e, i32 *const *f,
        const S *const t):
    a = 10
    c = NULL
    b[0] = 100
    s.member = 1000
    d = NULL
    e[0][0] = 1  # ok
    e[0] = NULL  # ok
    e = NULL     # nok
    f[0][0] = 1  # ok
    f[0] = NULL  # nok
    f = NULL     # ok
    t = &s

cdef volatile object v


_ERRORS = """
3:5: Const/volatile base type cannot be a Python object
8:5: Assignment to const 'x'
15:4: Assignment to const 'a'
16:4: Assignment to const 'c'
17:5: Assignment to const dereference
18:5: Assignment to const attribute 'member'
19:4: Assignment to const 'd'
22:4: Assignment to const 'e'
24:5: Assignment to const dereference
26:4: Assignment to const 't'
28:5: Const/volatile base type cannot be a Python object
"""
