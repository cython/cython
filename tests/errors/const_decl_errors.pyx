# mode: error
# tag: warnings
cdef const object o

cdef const int x = 10
x = 20           # nok

cdef const int y

y = 20 # ok

cdef const int xx = x
cdef const int xy = x
cdef const int *z

cdef float a[x]  # ok
cdef float aa[xx] # nok

cdef struct S:
    int member
    int[x] member2 #ok
    int[xy] member3 #nok

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

_ERRORS = """
3:5: Const/volatile base type cannot be a Python object
6:4: Assignment to const 'x'
12:0: Const variable used in array must be initialized with integer value!
13:0: Const variable used in array must be initialized with integer value!
26:8: Assignment to const 'a'
27:8: Assignment to const 'c'
28:5: Assignment to const dereference
29:5: Assignment to const attribute 'member'
30:8: Assignment to const 'd'
33:8: Assignment to const 'e'
35:5: Assignment to const dereference
37:8: Assignment to const 't'
41:8: Assignment to const 'y'
43:5: Assignment to const dereference
50:5: Const/volatile base type cannot be a Python object
67:14: Previous declaration is here
68:14: 'a' redeclared
"""

_WARNINGS = """
31:4: Assigning to 'int *' from 'const int *' discards const qualifier
34:11: Assigning to 'int *' from 'const int *' discards const qualifier
34:14: Assigning to 'int *' from 'const int *' discards const qualifier
35:12: Assigning to 'int *' from 'const int *' discards const qualifier
35:12: Assigning to 'int *' from 'const int *' discards const qualifier
"""
