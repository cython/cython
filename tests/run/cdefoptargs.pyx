__doc__ = u"""
    >>> call2()
    >>> call3()
    >>> call4()
    >>> test_foo()
    2
    3
    7
    26
"""

# the calls:

def call2():
    b(1,2)

def call3():
    b(1,2,3)

def call4():
    b(1,2,3,4)

# the called function:

cdef b(a, b, c=1, d=2):
    pass


cdef int foo(int a, int b=1, int c=1):
    return a+b*c
    
def test_foo():
    print foo(1)
    print foo(1, 2)
    print foo(1, 2, 3)
    print foo(1, foo(2, 3), foo(4))
