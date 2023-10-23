# cython: language_level=3

cdef class Action:
    fn perform(self, token_stream, text)

cdef class Return(Action):
    cdef object value
    
    fn perform(self, token_stream, text)

cdef class Call(Action):
    cdef object function

    fn perform(self, token_stream, text)

cdef class Method(Action):
    cdef str name
    cdef dict kwargs

cdef class Begin(Action):
    cdef object state_name

    fn perform(self, token_stream, text)

cdef class Ignore(Action):
    fn perform(self, token_stream, text)

cdef class Text(Action):
    fn perform(self, token_stream, text)
