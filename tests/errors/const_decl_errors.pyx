# mode: error
# tag: warnings

cdef const int x = 10
x = 20           # nok

cdef const int y
cdef const float yy = 5.0  # ok
cdef const float zz = 5.0 + 5.0 #ok
cdef const int i = y # nok

y = 20 # ok

cdef const int ii = y # nok

cdef const int xx = x # nok
cdef const int *z

cdef float a[x]     # nok
cdef float aa[xx]   # nok
cdef float aaa[yy]  # nok

cdef struct S:
    int member
    int[x] member2   # nok
    int[xx] member3  # nok
    int[yy] member4  # nok

cdef func(const int a, const int* b, const (int*) c, const S s, int *const d, int **const e, int *const *f,
          const S *const t):
    a = 10          # nok
    c = NULL        # nok
    b[0] = 100      # nok
    s.member = 1000 # nok
    d = NULL        # nok
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
    cdef int a[x]  # nok
    cdef int aa[xx] # nok

cdef const int int_sum_constant3 = 10 + x        # nok
cdef const float float_sum_constant2 = 50.2 + yy # nok
cdef char *const string2 = "string2"             # nok
cdef const char *const string3 = "string3"       # nok

_ERRORS = """
5:4: Assignment to const 'x'
10:0: Assignment to const 'i'
14:0: Assignment to const 'ii'
16:0: Assignment to const 'xx'
19:13: Array dimension cannot be const variable
20:14: Array dimension cannot be const variable
21:15: Array dimension cannot be const variable
21:15: Array dimension not integer
25:8: Array dimension cannot be const variable
26:8: Array dimension cannot be const variable
27:8: Array dimension cannot be const variable
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
72:15: Array dimension cannot be const variable
73:16: Array dimension cannot be const variable
75:0: Assignment to const 'int_sum_constant3'
76:0: Assignment to const 'float_sum_constant2'
"""

_WARNINGS = """
31:4: Assigning to 'int *' from 'const int *' discards const qualifier
34:11: Assigning to 'int *' from 'const int *' discards const qualifier
34:14: Assigning to 'int *' from 'const int *' discards const qualifier
35:12: Assigning to 'int *' from 'const int *' discards const qualifier
35:12: Assigning to 'int *' from 'const int *' discards const qualifier
"""
