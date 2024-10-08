# mode: error
# tag: warnings
cdef const object o # nok

cdef const int x = 10
x = 20           # nok

cdef const int y
cdef const float yy = 5.0

y = 20 # ok

cdef const int xx = x
cdef const int *z

cdef float a[x]     # ok
cdef float aa[xx]   # ok
cdef float aaa[yy]  # nok

cdef struct S:
    int member
    int[x] member2   # ok
    int[xx] member3  # ok
    int[yy] member4  # nok

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

cdef const_warn(const int *b, const int *c):
    cdef int *x = b
    cdef int *y
    cdef int *z
    y, z = b, c
    z = y = b

cdef const_ok(const int *b, const int *c):
    cdef const int *x = b
    cdef const int *y
    cdef const int *z
    y, z = b, c
    z = y = b

cdef func4():
    cdef int a[x] # ok
    cdef int a[xx] # nok

cdef const int int_sum_constant3 = 10 + x # nok
cdef const float float_sum_constant2 = 50.2 + yy # nok
cdef char *const string2 = "string2" # nok
cdef const char *const string3 = "string3" #nok

_ERRORS = """
3:5: Const/volatile base type cannot be a Python object
6:4: Assignment to const 'x'
18:15: Array dimension not integer
24:8: Array dimension not integer
28:8: Assignment to const 'a'
29:8: Assignment to const 'c'
30:5: Assignment to const dereference
31:5: Assignment to const attribute 'member'
32:8: Assignment to const 'd'
35:8: Assignment to const 'e'
37:5: Assignment to const dereference
39:8: Assignment to const 't'
43:8: Assignment to const 'y'
45:5: Assignment to const dereference
52:5: Const/volatile base type cannot be a Python object
69:14: Previous declaration is here
70:14: 'a' redeclared
72:0: Assignment to const 'int_sum_constant3'
73:0: Assignment to const 'float_sum_constant2'
74:0: Assignment to const 'string2'
75:0: Assignment to const 'string3'
"""

_WARNINGS = """
31:4: Assigning to 'int *' from 'const int *' discards const qualifier
34:11: Assigning to 'int *' from 'const int *' discards const qualifier
34:14: Assigning to 'int *' from 'const int *' discards const qualifier
35:12: Assigning to 'int *' from 'const int *' discards const qualifier
35:12: Assigning to 'int *' from 'const int *' discards const qualifier
"""
