# mode: compile

# the following are valid syntax constructs and should not produce errors

ctypedef int x;

cdef no_semi():
    cdef int i

cdef with_semi():
    cdef int i;

def use_cdef():
  &no_semi, &with_semi
