# mode: error

cdef const object o

cdef const int x = 10
x = 20           # nok

cdef const int y
cdef const int *z

cdef struct S:
    int member

cdef func(const int a, const int* b, const (int*) c, const S s, int *const d, int **const e, int *const *f,
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

cdef func2():
    global y, z
    y = 10       # nok
    z = &y       # ok
    z[0] = 10    # nok

cdef func3():
    y = 10       # ok
    z = &y       # ok
    z[0] = 10    # ok

cdef volatile object v


_ERRORS = """
3:5: Const/volatile base type cannot be a Python object
6:4: Assignment to const 'x'
16:8: Assignment to const 'a'
17:8: Assignment to const 'c'
18:5: Assignment to const dereference
19:5: Assignment to const attribute 'member'
20:8: Assignment to const 'd'
23:8: Assignment to const 'e'
25:5: Assignment to const dereference
27:8: Assignment to const 't'
31:8: Assignment to const 'y'
33:5: Assignment to const dereference
40:5: Const/volatile base type cannot be a Python object
"""
