__doc__ = u"""
>>> what()
0 5
>>> f(5)
>>> what()
42 5
>>> f(6)
>>> what()
42 6
>>> f("spam")
>>> what()
42 spam
"""

cdef int i = 0
cdef x = 5

def f(a):
    global i, x
    i = 42
    x = a

def what():
    print i,x
