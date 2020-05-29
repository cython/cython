import cython

@cython.locals(code0=cython.long, code1=cython.long)
cdef _add_transitions(dict state, event, new_state, cython.long maxint)
