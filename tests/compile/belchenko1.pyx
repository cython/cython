# mode: compile

cdef extern from *:
    ctypedef int intptr_t

cdef int _is_aligned(void *ptr):
    return ((<intptr_t>ptr) & ((sizeof(int))-1)) == 0

_is_aligned(NULL)
