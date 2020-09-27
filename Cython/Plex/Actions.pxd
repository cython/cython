# cython: language_level=3

cdef class Action:
    cdef perform(self, token_stream, text)
    cpdef same_as(self, other)

cdef class Return(Action):
    cdef public object value
    cdef perform(self, token_stream, text)
    cpdef same_as(self, other)

cdef class Call(Action):
    cdef public object function
    cdef perform(self, token_stream, text)
    cpdef same_as(self, other)

cdef class Method(Action):
    cdef public str name
    cdef public dict kwargs

cdef class Begin(Action):
    cdef public object state_name
    cdef perform(self, token_stream, text)
    cpdef same_as(self, other)

cdef class Ignore(Action):
    cdef perform(self, token_stream, text)

cdef class Text(Action):
    cdef perform(self, token_stream, text)
