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
7:4: Assignment to const 'x'
17:8: Assignment to const 'a'
18:8: Assignment to const 'c'
19:5: Assignment to const dereference
20:5: Assignment to const attribute 'member'
21:8: Assignment to const 'd'
24:8: Assignment to const 'e'
26:5: Assignment to const dereference
28:8: Assignment to const 't'
32:8: Assignment to const 'y'
34:5: Assignment to const dereference
41:5: Const/volatile base type cannot be a Python object
"""
