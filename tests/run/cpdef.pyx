cpdef void unraisable():
    """
    >>> unraisable()
    here
    """
    print('here')
    raise RuntimeError()

cpdef void raisable() except *:
    """
    >>> raisable()
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    print('here')
    raise RuntimeError()

cdef class A:
    """
    >>> A().foo()
    A
    """
    cpdef void foo(self):
        print "A"

cdef class B(A):
    """
    >>> B().foo()
    B
    """
    cpdef void foo(self):
        print "B"

class C(B):
    """
    >>> C().foo()
    C
    """
    def foo(self):
        print "C"
