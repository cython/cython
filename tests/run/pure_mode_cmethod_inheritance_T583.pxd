cdef class Base:
    cpdef str method(self)

cdef class Derived(Base):
    cpdef str method(self)
