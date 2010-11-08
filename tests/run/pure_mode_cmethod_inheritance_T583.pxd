cdef class Base:
    cpdef str noargs(self)
    cpdef str int_arg(self, int i)
    cpdef str _class(tp)

cdef class Derived(Base):
    cpdef str noargs(self)
    cpdef str int_arg(self, int i)
    cpdef str _class(tp)

cdef class DerivedDerived(Derived):
    cpdef str noargs(self)
    cpdef str int_arg(self, int i)
    cpdef str _class(tp)

cdef class Derived2(Base):
    cpdef str noargs(self)
    cpdef str int_arg(self, int i)
    cpdef str _class(tp)
