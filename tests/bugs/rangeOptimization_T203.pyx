__doc__ = u"""
>>> test_var(10, 5)
at 0
at 1
at 2
at 3
at 4
5
>>> test_func(5)
get_bound(5)
at 0
at 1
at 2
at 3
at 4
5
>>> test_f()
9
>>> f()
g called
0
1
2
2
"""

cdef int get_bound(int m):
    print "get_bound(%s)"%m
    return m

def test_var(int n, int m):
    cdef int i
    for i from 0 <= i < n:
        print "at", i
        n = m
    return i

def test_func(int n):
    cdef int i
    for i from 0 <= i < get_bound(n):
        print "at", i
    return i

def test_f():
    cdef int i,n
    n = 10
    for i in range(n):
      if i == 5: n *= 2
    print i

cdef int g():
    print "g called"
    return 3

def f():
    cdef int i
    for i in range(g()):
        print i
    print i

