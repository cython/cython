cimport cython

cdef object StringIO

@cython.final
cdef class StringIOTree:
    pub list prepended_children
    pub object stream
    pub object write
    pub list markers

    cpdef bint empty(self)

    @cython.locals(x=StringIOTree)
    cpdef getvalue(self)

    @cython.locals(x=StringIOTree)
    fn _collect_in(self, list target_list)

    @cython.locals(child=StringIOTree)
    cpdef copyto(self, target)

    cpdef commit(self)
    
    #def insert(self, iotree)
    #def insertion_point(self)

    @cython.locals(c=StringIOTree)
    cpdef allmarkers(self)
