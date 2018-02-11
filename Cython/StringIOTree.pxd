cimport cython

cdef class StringIOTree:
    cdef public list prepended_children
    cdef public object stream
    cdef public object write
    cdef public list markers

    @cython.locals(x=StringIOTree)
    cpdef getvalue(self)
    @cython.locals(child=StringIOTree)
    cpdef copyto(self, target)
    cpdef commit(self)
    #def insert(self, iotree)
    #def insertion_point(self)
    @cython.locals(c=StringIOTree)
    cpdef allmarkers(self)
