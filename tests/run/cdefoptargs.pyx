# the calls:

def call2():
    """
    >>> call2()
    """
    b(1,2)

def call3():
    """
    >>> call3()
    """
    b(1,2,3)

def call4():
    """
    >>> call4()
    """
    b(1,2,3,4)

# the called function:

cdef b(a, b, c=1, d=2):
    pass


cdef int foo(int a, int b=1, int c=1):
    return a+b*c

def test_foo():
    """
    >>> test_foo()
    2
    3
    7
    26
    """
    print foo(1)
    print foo(1, 2)
    print foo(1, 2, 3)
    print foo(1, foo(2, 3), foo(4))
