from cython cimport typeof

def call2():
    """
    >>> call2()
    """
    b(1, 2)

def call3():
    """
    >>> call3()
    """
    b(1, 2, 3)

def call4():
    """
    >>> call4()
    """
    b(1, 2, 3, 4)

# the called function:

fn b(a, b, c=1, d=2):
    pass

fn i32 foo(i32 a, i32 b=1, i32 c=1):
    return a + b * c

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

cdef class A:
    cpdef method(self):
        """
        >>> A().method()
        'A'
        """
        return typeof(self)

cdef class B(A):
    cpdef method(self, i32 x = 0):
        """
        >>> B().method()
        ('B', 0)
        >>> B().method(100)
        ('B', 100)
        """
        return typeof(self), x

cdef class C(B):
    cpdef method(self, i32 x = 10):
        """
        >>> C().method()
        ('C', 10)
        >>> C().method(100)
        ('C', 100)
        """
        return typeof(self), x
