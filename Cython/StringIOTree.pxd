cimport cython

cdef object StringIO

@cython.final
cdef class StringIOTree:
    cdef public list prepended_children
    cdef public object stream
    cdef public object write
    cdef public list markers

    cpdef bint empty(self)
    @cython.locals(x=StringIOTree)
    cpdef getvalue(self)
    @cython.locals(x=StringIOTree)
    cdef _collect_in(self, list target_list)
    @cython.locals(child=StringIOTree)
    cpdef copyto(self, target)
    cpdef commit(self)
    #def insert(self, iotree)
    #def insertion_point(self)
    @cython.locals(c=StringIOTree)
    cpdef allmarkers(self)
