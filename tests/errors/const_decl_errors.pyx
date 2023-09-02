# mode: error
# tag: warnings
cdef const object o

cdef const int x = 10
x = 20           # nok

cdef const int y
cdef const int *z

cdef float a[x] #nok

cdef struct S:
    int member
    int[x] member2 #nok

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
    cdef int a[x] # nok

_ERRORS = """
3:5: Const/volatile base type cannot be a Python object
6:4: Assignment to const 'x'
11:13: Array dimension cannot be const integer
15:8: Array dimension cannot be const integer
19:8: Assignment to const 'a'
20:8: Assignment to const 'c'
21:5: Assignment to const dereference
22:5: Assignment to const attribute 'member'
23:8: Assignment to const 'd'
26:8: Assignment to const 'e'
28:5: Assignment to const dereference
30:8: Assignment to const 't'
34:8: Assignment to const 'y'
36:5: Assignment to const dereference
43:5: Const/volatile base type cannot be a Python object
60:15: Array dimension cannot be const integer
"""

_WARNINGS = """
31:4: Assigning to 'int *' from 'const int *' discards const qualifier
34:11: Assigning to 'int *' from 'const int *' discards const qualifier
34:14: Assigning to 'int *' from 'const int *' discards const qualifier
35:12: Assigning to 'int *' from 'const int *' discards const qualifier
35:12: Assigning to 'int *' from 'const int *' discards const qualifier
"""
