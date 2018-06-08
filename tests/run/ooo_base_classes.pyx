cdef class B(A):
  cpdef foo(self):
    """
    >>> B().foo()
    B
    """
    print "B"

cdef class A(object):
  cpdef foo(self):
    """
    >>> A().foo()
    A
    """
    print "A"

cdef class C(A):
  cpdef foo(self):
    """
    >>> C().foo()
    C
    """
    print "C"
