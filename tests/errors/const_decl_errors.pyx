# mode: error

cdef const object o

# TODO: This requires making the assignment at declaration time.
# (We could fake this case by dropping the const here in the C code,
# as it's not needed for agreeing with external libraries.
cdef const int x = 10

cdef struct S:
    int member

cdef func(const int a, const int* b, const (int*) c, const S s, int *const d,
          const S *const t):
    a = 10
    c = NULL
    b[0] = 100
    s.member = 1000
    d = NULL
    t = &s


_ERRORS = """
3:5: Const base type cannot be a Python object
8:5: Assignment to const 'x'
15:4: Assignment to const 'a'
16:4: Assignment to const 'c'
17:5: Assignment to const dereference
18:5: Assignment to const attribute 'member'
19:4: Assignment to const 'd'
20:4: Assignment to const 't'
"""
