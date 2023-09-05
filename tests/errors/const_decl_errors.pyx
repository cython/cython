# mode: error

cdef const object o # nok

cdef const int x = 10

cdef const int y
cdef const int *z
cdef const double dx = 5.1

x = 20           # nok
cdef float a[x]  # ok
cdef float b[dx] # nok

cdef struct S:
    int member
    int[x] member2 #ok

cdef func(const int a, const int* b, const (int*) c, const S s, int *const d, int **const e, int *const *f,
          const S *const t):
    a = 10      # nok
    c = NULL    # nok
    b[0] = 100  # nok
    s.member = 1000 # nok
    d = NULL     # nok
    e[0][0] = 1  # ok
    e[0] = NULL  # ok
    e = NULL     # nok
    f[0][0] = 1  # ok
    f[0] = NULL  # nok
    f = NULL     # ok
    t = &s       # nok

cdef func2():
    global y, z
    y = 10       # nok
    z = &y       # ok
    z[0] = 10    # nok

cdef func3():
    y = 10       # ok
    z = &y       # ok
    z[0] = 10    # ok

cdef volatile object v # nok

cdef func4():
    cdef int a[x] # ok

_ERRORS = """
3:5: Const/volatile base type cannot be a Python object
11:4: Assignment to const 'x'
13:13: Array dimension not integer
21:8: Assignment to const 'a'
22:8: Assignment to const 'c'
23:5: Assignment to const dereference
24:5: Assignment to const attribute 'member'
25:8: Assignment to const 'd'
28:8: Assignment to const 'e'
30:5: Assignment to const dereference
32:8: Assignment to const 't'
36:8: Assignment to const 'y'
38:5: Assignment to const dereference
45:5: Const/volatile base type cannot be a Python object
"""
