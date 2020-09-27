# mode: compile
# tag: warnings

# Test detection of obvious cases where the user intended to use a cdef function but failed to type it

cdef class C:
    cdef int val1
    cdef public int val2
    cdef int func1(self):
        return 1
    cpdef int func2(self) except *:
        return 2
    def func3(self):
        return 3

def f():
    cdef c = C()
    c.func1()
    c.func2()
    c.func3()
    c.val1 = 5
    c.val2 = 5

def getC():
    return C()

def g():
    getC().func1()
    getC().func2()
    getC().func3()
    getC().val1 = 5
    getC().val2 = 5

cdef c = C()
c.func1()
c.func2()
c.func3()
c.val1 = 5
c.val2 = 5

_WARNINGS = """
18:5: 'c' is typed as a Python object; if you intended to lookup 'C.func1' then you must specify the type of 'c'
19:5: 'c' is typed as a Python object; to enable fast C lookup of 'C.func2' then you must specify the type of 'c'
21:5: 'c' is typed as a Python object; if you intended to lookup 'C.val1' then you must specify the type of 'c'
22:5: 'c' is typed as a Python object; to enable fast C lookup of 'C.val2' then you must specify the type of 'c'
28:10: This expression is typed as a Python object; if you intended to lookup 'C.func1' then you must specify the type of this expression
29:10: This expression is typed as a Python object; to enable fast C lookup of 'C.func2' then you must specify the type of this expression
31:10: This expression is typed as a Python object; if you intended to lookup 'C.val1' then you must specify the type of this expression
32:10: This expression is typed as a Python object; to enable fast C lookup of 'C.val2' then you must specify the type of this expression
35:1: 'c' is typed as a Python object; if you intended to lookup 'C.func1' then you must specify the type of 'c'
36:1: 'c' is typed as a Python object; to enable fast C lookup of 'C.func2' then you must specify the type of 'c'
38:1: 'c' is typed as a Python object; if you intended to lookup 'C.val1' then you must specify the type of 'c'
39:1: 'c' is typed as a Python object; to enable fast C lookup of 'C.val2' then you must specify the type of 'c'
# BUG:
11:10: 'func2' redeclared
"""
