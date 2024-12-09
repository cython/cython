# mode: error
# tag: warnings
cdef const object o # nok

cdef const int x = 10
x = 20           # nok

cdef const int y
cdef const float yy = 5.0
cdef const int i = y # nok

y = 20 # ok

cdef const int ii = y # ok

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
10:0: Const variable 'i' is not initialized
21:15: Array dimension not integer
27:8: Array dimension not integer
31:8: Assignment to const 'a'
32:8: Assignment to const 'c'
33:5: Assignment to const dereference
34:5: Assignment to const attribute 'member'
35:8: Assignment to const 'd'
38:8: Assignment to const 'e'
40:5: Assignment to const dereference
42:8: Assignment to const 't'
46:8: Assignment to const 'y'
48:5: Assignment to const dereference
55:5: Const/volatile base type cannot be a Python object
72:14: Previous declaration is here
73:14: 'a' redeclared
75:0: Assignment to const 'int_sum_constant3'
76:0: Assignment to const 'float_sum_constant2'
77:0: Assignment to const 'string2'
78:0: Assignment to const 'string3'
"""

_WARNINGS = """
31:4: Assigning to 'int *' from 'const int *' discards const qualifier
34:11: Assigning to 'int *' from 'const int *' discards const qualifier
34:14: Assigning to 'int *' from 'const int *' discards const qualifier
35:12: Assigning to 'int *' from 'const int *' discards const qualifier
35:12: Assigning to 'int *' from 'const int *' discards const qualifier
"""
