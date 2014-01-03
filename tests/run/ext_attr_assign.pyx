# mode: run
# tag: assign, exttype

cdef struct X:
    int ix
    X* x


cdef class A:
    cdef int i
    cdef list l
    cdef object o
    cdef X x

    def assign_A(self):
        """
        >>> A().assign_A()
        (2, [1, 2, 3])
        """
        a = A()
        a.i = 1
        a.l = [1, 2, 3]
        a.o = a.l
        a.o = a.o
        a.l = a.o
        a.i = a.l[1]
        return a.i, a.l

    def assign_A_struct(self):
        """
        >>> A().assign_A_struct()
        (5, 2, 2, 5)
        """
        cdef X x
        a = A()
        a.x.ix = 2
        a.x.x = &x
        x.ix = 5
        x.x = &a.x
        assert a.x.x.x is &a.x

        a.x.x.x.x.x.x.x = a.x.x.x.x
        assert x.x is &x
        assert x.x.x is &x
        assert a.x.x is &x

        a.x.x.x.x.x.x.x, a.x.x.x = a.x.x.x.x, &a.x   # replay+undo :)
        assert x.x is &a.x
        assert x.x.x is &x
        return x.ix, x.x.ix, a.x.ix, a.x.x.ix


cdef class B(A):
    cdef int ib
    cdef object ob
    cdef A a

    def assign_B(self):
        """
        >>> B().assign_B()
        (1, 2, 5, 9, 2)
        """
        b = B()
        b.i = 1
        b.ib = 2
        b.l = [b.i, b.ib]
        b.o = b.l
        b.ob = b.o
        assert b.ob == b.l
        b.o = b.ob = b.l

        b.a = A()   # only one reference!
        b.a.o = 5
        b.a.i = 5
        b.a, b.a.i = A(), b.a.i  # overwrite b.a but keep b.a.i
        assert b.a.i == 5
        assert b.a.o is None
        b.a.o = 9
        b.a, b.a.i, b.a.o = A(), b.a.i, b.a.o
        return b.i, b.ib, b.a.i, b.a.o, b.o[1]

    def cross_assign_Ba(self):
        """
        >>> B().cross_assign_Ba()
        2
        """
        b = B()
        b.a = A()
        b.a.i = 1
        b.a.o = A()   # only one reference!
        (<A>b.a.o).i = 2
        b.a = b.a.o
        return b.a.i

    def cascaded_assign_B(self):
        """
        >>> B().cascaded_assign_B()
        (2, 2)
        """
        cdef B b = B()
        b.ib = 1
        b.a = A()
        b.a.o = B()   # only one reference!
        (<B>b.a.o).ib = 2
        b = b.ob = b.a.o
        return b.ib, (<B>b.ob).ib
